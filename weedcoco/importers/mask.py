from pathlib import Path
from typing import Mapping, Optional, Iterable, Tuple
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
from weedcoco.utils import add_metadata_from_file


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
        COCO segmentation string in compressed RLE format
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


def generate_mask_and_image_paths(
    image_dir: Path,
    mask_dir: Path,
    image_to_mask_pattern: Optional[str] = None,
    on_missing_mask: str = "error",
):
    """Collects masks corresponding to images in a directory

    Parameters
    ----------
    image_dir : pathlib.Path
    mask_dir : pathlib.Path
        Filenames should be identical to those in image-dir except for .png
        extension, unelss image_to_mask_pattern is given.
    image_to_mask_pattern : str, optional
        A regular expression that will match a substring of an image filename.
        The matched portion will have ".png" added and will be sought in
        mask_dir.
    on_missing_mask : one of {"error", "skip", "warn"}, default="error"
        If there is no mask available for a given image file, by default an
        error will be raised.  This allows it to instead be skipped.

    Yields
    ------
    mask_path : str
    image_path : str
    """
    if not image_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {image_dir}")
    if not mask_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {mask_dir}")
    if image_to_mask_pattern is None:
        image_to_mask_pattern = r"$.*\.(?=[^.]+$)"

    def _image_name_to_mask(name):
        try:
            return re.search(image_to_mask_pattern, name).group() + ".png"
        except AttributeError:
            raise ValueError(
                f"Could not extract mask filename from {name} "
                f"using pattern {repr(image_to_mask_pattern)}"
            )

    all_paths = sorted(image_dir.glob("*.*"))
    for path in all_paths:
        if path.name.startswith("."):
            # real glob excludes these
            continue
        mask_path = mask_dir / (_image_name_to_mask(path.name))
        if not mask_path.exists():
            if on_missing_mask == "error":
                raise FileNotFoundError(
                    f"No mask found at {mask_path} for image named {path.name}."
                )
            elif on_missing_mask == "warn":
                warnings.warn(
                    f"No mask found at {mask_path} for image named {path.name}."
                )
            continue

        yield mask_path, path

    if not all_paths:
        raise ValueError(f"No images found in {image_dir}")


def generate_paths_from_mask_only(mask_dir: Path, image_ext: str = "jpg"):
    """Generates image filenames corresponding to masks in a directory

    Parameters
    ----------
    mask_dir : pathlib.Path
    image_ext : str
        The extension to append to each mask path's stem to produce its
        corresponding image filename.

    Yields
    ------
    mask_path : str
    image_path : str
    """
    all_paths = sorted(mask_dir.glob("*.*"))
    for mask_path in all_paths:
        if mask_path.name.startswith("."):
            # real glob excludes these
            continue
        image_file_name = f"{mask_path.stem}.{image_ext}"
        yield mask_path, image_file_name

    if not all_paths:
        raise ValueError(f"No masks found in {mask_dir}")


class DefaultColorMapping(dict):
    def __init__(self, background_color):
        self.background_color = background_color

    def __missing__(self, k):
        if k == self.background_color:
            raise KeyError(k)
        out = self[k] = len(self)
        return out


def masks_to_coco(
    path_pairs: Iterable[Tuple[str, str]],
    color_to_category_map: Optional[Mapping[str, str]] = None,
    background_if_unmapped: Optional[str] = None,
    check_consistent_dimensions: bool = True,
):
    """Converts images and masks to MS COCO images and annotations

    Parameters
    ----------
    path_pairs : Iterable
        Pairs of (mask_path, image_path). mask_path needs to be readable,
        while image_path is copied verbatim into the COCO output.
    color_to_category_map : Mapping, optional
        Maps colours of format "RRGGBB" to valid WeedCOCO category names
    background_if_unmapped : str, optional
        Must be given if color_to_category_map is not. If not None, category
        names are set to hexadecimal colour values, rather than being mapped.
        The colour hex provided as `background_if_unmapped` will be treated as
        the background colour and will not be mapped.
    check_consistent_dimensions : bool, default=True
        Whether to check images and masks match in size. Should be false if
        images are not available.

    Returns
    -------
    dict
        Keys present should be 'images', 'annotations', and
        'categories'.
        Other COCO components should be added as a post-process.
    """
    if background_if_unmapped:
        color_to_idx_map = DefaultColorMapping(background_if_unmapped)
    else:
        categories = []
        color_to_idx_map = {}
        for i, (color, name) in enumerate(color_to_category_map.items()):
            categories.append({"id": i, "name": name})
            color_to_idx_map[color.lower()] = i

    images = []
    annotations = []
    colors_not_found = set()
    categories_found = set()
    for mask_path, image_path in path_pairs:
        dims = get_image_dimensions(mask_path)
        if check_consistent_dimensions and get_image_dimensions(image_path) != dims:
            raise ValueError(
                f"Got inconsistent dimensions for image "
                f"({get_image_dimensions(image_path)}) and mask ({dims})"
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

        images.append({"id": len(images), "file_name": Path(image_path).name, **dims})

    if background_if_unmapped:
        categories = [{"id": v, "name": k} for k, v in color_to_idx_map.items()]

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
            f"These categories were not found: {missing_category_colors}"
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
    ap.add_argument(
        "--mask-dir",
        required=True,
        type=Path,
        help="Filenames should be identical to those in image-dir, with extensions replaced by PNG",
    )
    image_dir_meg = ap.add_mutually_exclusive_group(required=True)
    image_dir_meg.add_argument("--image-dir", type=Path)
    image_dir_meg.add_argument(
        "--image-ext",
        type=str,
        help=(
            "The filename extension (excl .) to apply to mask file names "
            "to generate an image file name."
        ),
    )

    cat_group = ap.add_mutually_exclusive_group(required=True)
    cat_group.add_argument(
        "-C",
        "--category-map",
        type=Path,
        help=(
            "JSON or YAML mapping of colors (RRGGBB) to WeedCOCO category names. "
            "The background color should not be mapped."
        ),
    )
    cat_group.add_argument(
        "-U",
        "--unmapped-on-black",
        action="store_const",
        dest="background_if_unmapped",
        const="000000",
        help=(
            "Do not map the colours, and output hex colours as COCO category "
            "names. Assume the background is black."
        ),
    )

    ap.add_argument("--agcontext-path", type=Path)
    ap.add_argument("--metadata-path", type=Path)
    ap.add_argument("--validate", action="store_true", default=False)
    ap.add_argument("-o", "--out-path", default="coco_from_mask.json", type=Path)
    ap.add_argument(
        "-P",
        "--path-to-mask-pattern",
        default=None,
        help="Pattern to extract mask name from image path when using --image-dir",
    )
    ap.add_argument(
        "--on-missing-mask",
        choices={"skip", "warn", "error"},
        help=(
            "Whether to 'skip', 'warn', or 'error' if the matching "
            "mask can not be found when --image-dir is used"
        ),
    )
    args = ap.parse_args(args)

    if args.image_ext:
        path_pairs = generate_paths_from_mask_only(args.mask_dir, args.image_ext)
        check_consistent_dimensions = False
    else:
        path_pairs = generate_mask_and_image_paths(
            args.image_dir,
            args.mask_dir,
            image_to_mask_pattern=args.path_to_mask_pattern,
            on_missing_mask=args.on_missing_mask,
        )
        check_consistent_dimensions = True

    if args.category_map is None:
        color_to_category_map = None
    else:
        color_to_category_map = load_json_or_yaml(args.category_map)
    coco = masks_to_coco(
        path_pairs,
        color_to_category_map,
        check_consistent_dimensions=check_consistent_dimensions,
        background_if_unmapped=args.background_if_unmapped,
    )

    if args.agcontext_path:
        add_agcontext_from_file(coco, args.agcontext_path)
    if args.metadata_path:
        add_metadata_from_file(coco, args.metadata_path)

    if args.validate:
        validate(coco)

    with args.out_path.open("w") as out:
        json.dump(coco, out, indent=4)


if __name__ == "__main__":
    main()
