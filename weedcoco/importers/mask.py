from pathlib import Path
from typing import Mapping
import argparse
import json
import warnings
import re

import PIL.Image
import numpy as np
import pycocotools.mask

from weedcoco.validation import validate
from weedcoco.utils import load_json_or_yaml
from weedcoco.utils import get_image_dimensions
from weedcoco.utils import add_agcontext_from_file
from weedcoco.utils import add_collection_from_file


def generate_segmentations(mask_path, color_map, colors_not_found):
    """
    Parameters
    ----------
    mask_path : pathlib.Path or str
    color_map : Mapping
        Maps lowercase 6-character hex color string to some value
    colors_not_found : set
        Colors are added here, as 6-character hex values, if found in mask, but
        not in color_map.

    Yields
    ------
    segmentation : str
        COCO segmentation string
    category
        Value from color_map
    """
    im = PIL.Image.open(str(mask_path))
    width, height = im.size
    distinct_colours, digitized = np.unique(
        np.reshape(im, (-1, 3)), return_inverse=True, axis=0
    )
    digitized = digitized.reshape(height, width)
    del im

    for i, color_rgb in enumerate(distinct_colours):
        color_hex = "%02x%02x%02x" % tuple(color_rgb)
        try:
            category = color_map[color_hex]
        except KeyError:
            colors_not_found.add(color_hex)
            continue
        segmentation = pycocotools.mask.encode(np.asfortranarray(digitized == i))
        segmentation["counts"] = segmentation["counts"].decode("ascii")
        yield segmentation, category


def masks_to_coco(
    image_dir: Path,
    mask_dir: Path,
    color_to_category_map: Mapping[str, str],
    image_to_mask_pattern=None,
):
    """Converts images and masks to MS COCO images and annotations

    Parameters
    ----------
    image_dir : pathlib.Path
    mask_dir : pathlib.Path
        Filenames should be identical to those in image-dir except for .png
        extension, unelss image_to_mask_pattern is given.
    color_to_category_map : Mapping
        Maps colours of format "RRGGBB" to valid WeedCOCO category names
    image_to_mask_pattern : str
        A regular expression that will match a substring of an image filename.
        The matched portion will have ".png" added and will be sought in
        mask_dir.

    Returns
    -------
    dict
        Keys present should be 'images', 'annotations', and
        'categories'.
        Other COCO components should be added as a post-process.
    """
    if not image_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {image_dir}")
    if not mask_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {mask_dir}")
    if image_to_mask_pattern is None:
        image_to_mask_pattern = r"$.*\.(?=[^.]+$)"

    categories = []
    color_to_idx_map = {}
    for i, (color, name) in enumerate(color_to_category_map.items()):
        categories.append({"id": i, "name": name})
        color_to_idx_map[color.lower()] = i

    def _image_name_to_mask(name):
        try:
            return re.search(image_to_mask_pattern, name).group() + ".png"
        except AttributeError:
            raise ValueError(
                f"Could not extract mask filename from {name} "
                f"using pattern {repr(image_to_mask_pattern)}"
            )

    images = []
    annotations = []
    colors_not_found = set()
    categories_found = set()
    for path in image_dir.glob("*.*"):
        mask_path = mask_dir / (_image_name_to_mask(path.name))
        if not mask_path.exists():
            raise FileNotFoundError(
                f"Found image named {path.name} but no mask at {mask_path}"
            )
        dims = get_image_dimensions(mask_path)
        if get_image_dimensions(path) != dims:
            raise ValueError(
                f"Got inconsistent dimensions for image "
                f"({get_image_dimensions(path)}) and mask ({dims})"
            )

        segmentations = generate_segmentations(
            mask_path, color_to_idx_map, colors_not_found
        )
        for rle, cat_idx in segmentations:
            categories_found.add(cat_idx)
            bbox = list(map(int, pycocotools.mask.toBbox(rle)))
            annotation = {
                "id": len(annotations),
                "image_id": len(images),
                "category_id": cat_idx,
                "segmentation": rle,
                # "is_crowd": 0,  # TODO: how should we define this?
                "bbox": bbox,
            }
            annotations.append(annotation)

        images.append({"id": len(images), "file_name": path.name, **dims})

    if not images:
        raise ValueError(f"No images found in {image_dir}")

    if len(colors_not_found) > 1:
        raise ValueError(
            f"Expected at most one color to not be mapped to a category. "
            f"Got {len(colors_not_found)}: {', '.join(f'#{x}' for x in sorted(colors_not_found))}."
        )
    if len(categories_found) != len(categories):
        missing_category_names = {
            cat["name"] for cat in categories if cat["id"] not in categories_found
        }
        missing_category_colors = {
            color: name
            for color, name in color_to_category_map.items()
            if name in missing_category_names
        }

        warnings.warn(
            f"{len(categories)} categories defined, but only "
            f"{len(categories_found)} of these are present in masks. "
            f"Missing are {missing_category_colors}"
        )

    out = {
        "images": images,
        "annotations": annotations,
        "info": {},
        "categories": categories,
    }

    return out


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--image-dir", required=True, type=Path)
    ap.add_argument(
        "--mask-dir",
        required=True,
        type=Path,
        help="Filenames should be identical to those in image-dir, with extensions replaced by PNG",
    )
    ap.add_argument("-P", "--path-to-mask-pattern", default=None)
    ap.add_argument(
        "-C",
        "--category-map",
        required=True,
        type=Path,
        help=(
            "JSON or YAML mapping of colors (RRGGBB) to WeedCOCO category names. "
            "The background color should not be mapped."
        ),
    )
    ap.add_argument("--agcontext-path", type=Path)
    ap.add_argument("--collection-path", type=Path)
    ap.add_argument("--validate", action="store_true", default=False)
    ap.add_argument("-o", "--out-path", default="coco_from_mask.json", type=Path)
    args = ap.parse_args(args)

    color_to_category_map = load_json_or_yaml(args.category_map)
    coco = masks_to_coco(
        args.image_dir,
        args.mask_dir,
        color_to_category_map,
        image_to_mask_pattern=args.path_to_mask_pattern,
    )

    if args.agcontext_path:
        add_agcontext_from_file(coco, args.agcontext_path)
    if args.collection_path:
        add_collection_from_file(coco, args.collection_path)

    if args.validate:
        validate(coco)

    with args.out_path.open("w") as out:
        json.dump(coco, out, indent=4)


if __name__ == "__main__":
    main()
