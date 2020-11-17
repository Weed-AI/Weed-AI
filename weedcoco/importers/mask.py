from collections import defaultdict
from pathlib import Path
from typing import Optional, Mapping
import argparse
import json

from lxml import etree

import cv2 as cv
import numpy as np
import os

from weedcoco.validation import validate
from weedcoco.utils import load_json_or_yaml
from weedcoco.utils import add_agcontext_from_file
from weedcoco.utils import add_collection_from_file

# TODO: extend functionality to read categories from a file
categories = [
    {"id": 0, "name": "other: background", "colour":[0,0,0]},
    {"id": 1, "name": "weed: rapistrum rugosum", "colour":[255,0,0]},
    {"id": 2, "name": "crop: triticum aestivum", "colour":[0,255,0]},
    {"id": 3, "name": "weed: lolium rigidum", "colour":[0,0,255]}
]
def mask_to_segment(distinct_colours):
    segment["segment"] = pycocotools.mask.encode(np.asfortranarray((arr == distinct_colours).all(axis=-1)))
    return segment
    
def colours_to_categories(category_name_map):
    keys, values = zip(*category_name_map.items())
    categories = [{"id": i, "name": value} for i, value in enumerate(values)]
    category_mapping = {key: i for i, key in enumerate(keys)}
    for key, value in category_name_map.items():
        category_name_map[key] = ImageColor.getcolor(key, "RGB")
        
    return category_name_map

def generate_masks_segmentations(distinct_colours):
    def np_tolist(np_array):
        return np_array.tolist()

    segments = []
    for color in distinct_colours:
        segment = pycocotools.mask.encode(np.asfortranarray((arr == distinct_colours[color])))
        segments.append(segment)
   
    return json.dumps(list(map(np_tolist, segments)))


def mask_to_coco(image_dir: Path, mask_dir: Path):

    """Converts images and masks to MS COCO images and annotations

    Parameters
    ----------
    image_dir: pathlib.Path
    mask_dir: pathlib.Path

    Returns
    -------
    dict
        Keys present should be 'images', 'annotations', and
        'categories'.
        Other COCO components should be added as a post-process.
    """
    use_default_category_mapping = category_mapping is None
    if use_default_category_mapping:
        category_mapping = defaultdict(None)
        # ordinal numbering
        category_mapping.default_factory = category_mapping.__len__

    images = []
    annotations = []

    image_id = 0
    for filename in os.listdir(image_dir):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            coco_image = {
                "id": image_id,
                "file_name": filename,
            }  # TODO: use get_image_dimensions
            images.append(coco_image)

            annotation = {
                "id": image_id,
                "image_id": image_id,
                "category_id": 0,
                "segmentation": generate_segments(str(mask_dir / filename)),
                "is_crowd": 0,
            }
            annotations.append(annotation)
            image_id += 1

    out = {
        "images": images,
        "annotations": annotations,
        "info": {},
        "categories": categories,
    }

    return out


# TODO: Add licenses


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--image-dir", required=True, type=Path)
    ap.add_argument("--mask-dir", required=True, type=Path)
        ap.add_argument(
        "--category-name-map",
        type=Path,
        help="JSON or YAML mapping of VOC names to WeedCOCO category names",
    )
    ap.add_argument("--agcontext-path", type=Path)
    ap.add_argument("--collection-path", type=Path)
    ap.add_argument("--validate", action="store_true", default=False)
    ap.add_argument("-o", "--out-path", default="coco_from_mask.json", type=Path)
    args = ap.parse_args(args)

    coco = mask_to_coco(args.image_dir, args.mask_dir)

    if categories is not None:
        coco["categories"] = categories
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
