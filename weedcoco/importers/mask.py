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

categories = [
        {
            "id": 0,
            "name": "crop: zingiber officnale"
        },
    ]

def mask_to_coco(image_dir: Path, mask_dir: Path):

    images = []
    annotations = []

    image_id = 0
    for filename in os.listdir(image_dir):
        if filename.endswith(".png") or filename.endswith(".jpg"): 
            coco_image = {
                "id": image_id,
                "file_name": filename,
            }
            images.append(coco_image)

            annotation = {
                "id": image_id,
                "category_id": 0,
                "contours": generate_masks_contours(str(mask_dir / filename)),
            }
            annotations.append(annotation)
            image_id += 1

    out = {
        "images": images,
        "annotations": annotations,
        "info": {},
        "categories": categories
    }

    return out

def generate_masks_contours(mask_path):

    """
    Return contours' matrix of mask or image using opencv
    """
    def np_tolist(np_array):
        return np_array.tolist()

    im = cv.imread(mask_path)
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    return json.dumps(list(map(np_tolist, contours)))


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--image-dir", required=True, type=Path)
    ap.add_argument("--mask-dir", required=True, type=Path)
    ap.add_argument("--agcontext-path", type=Path)
    ap.add_argument("--collection-path", type=Path)
    ap.add_argument("--validate", action="store_true", default=False)
    ap.add_argument("-o", "--out-path", default="coco_from_mask.json", type=Path)
    args = ap.parse_args(args)

    coco = mask_to_coco(args.image_dir, args.mask_dir)

    if not coco["images"]:
        ap.error(f"Found no .xml files in {args.voc_dir}")

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
