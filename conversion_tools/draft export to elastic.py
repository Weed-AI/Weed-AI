#!/usr/bin/env python
# coding: utf-8
# Exports Weed COCO on stdin to ElasticSearch _bulk data on stdout

import sys
import json
import argparse
import os
import logging

log = logging.getLogger()
logging.basicConfig(level=logging.INFO)

ap = argparse.ArgumentParser()
ap.add_argument(
    "--thumbnail-dir", help="Replace the input file_name directory with this"
)
args = ap.parse_args()

coco = json.load(sys.stdin)
del coco["info"]
try:
    del coco["collection_memberships"]
except KeyError:
    pass

id_lookup = {}
for key, objs in coco.items():
    log.info(f"Mapping {len(objs)} {key}")
    for obj in objs:
        id_lookup[key, obj["id"]] = obj


def _flatten(src, dst, prefix):
    for k, v in src.items():
        dst[f"{prefix}__{k}"] = v


for annotation in coco["annotations"]:
    image = id_lookup["images", annotation["image_id"]]
    image.setdefault("annotations", []).append(annotation)
    annotation["category"] = id_lookup["categories", annotation["category_id"]]
    _flatten(annotation["category"], annotation, "category")
    # todo: add collection from collection_memberships
    if hasattr(args, "thumbnail_dir"):
        image["thumbnail"] = (
            args.thumbnail_dir + "/" + os.path.basename(image["file_name"])
        )
    else:
        image["thumbnail"] = image["file_name"]

for image in coco["images"]:
    image["agcontext"] = id_lookup["agcontexts", image["agcontext_id"]]
    _flatten(image["agcontext"], image, "agcontext")
    # todo: add license
    for annotation in image["annotations"]:
        for k in annotation:
            image.setdefault(f"annotation__{k}", []).append(annotation[k])

# Code derived from Olivier Melançon's answer https://stackoverflow.com/questions/55892600/python-triplet-dictionary
class GroupMap:
    def __init__(self):
        self.data = {}

    def add(self, group):
        for item in group:
            self.data[item] = group

    def __getitem__(self, item):
        return self.data[item]


# A dictionary of value triplets
growth = {
    ("emergence", "germination", "^gs0[0-9]$"),
    ("emergence", "sprouting", "^gs0[0-9]$"),
    ("emergence", "bud development", "^gs0[0-9]$"),
    ("seedling", "leaf development", "^gs1[0-9]$"),
    ("tillering", "formation of side roots", "^gs2[0-9]$"),
    ("tillering", "tillering", "^gs2[0-9]$"),
    ("stem elongation", "stem elongation", "^gs3[0-9]$"),
    ("stem elongation", "rosette growth", "^gs3[0-9]$"),
    ("stem elongation", "shoot development", "^gs3[0-9]$"),
    ("booting", "development of harvestable vegetable parts", "^gs4[0-9]$"),
    ("booting", "bolting", "^gs4[0-9]$"),
    ("ear emergence", "inflorescence", "^gs5[0-9]$"),
    ("ear emergence", "emergence", "^gs5[0-9]$"),
    ("ear emergence", "heading", "^gs5[0-9]$"),
    ("flowering", "flowering", "^gs6[0-9]$"),
    ("milky dough", "development of fruit", "^gs7[0-9]$"),
    ("dough", "ripening or maturity of fruit and seed", "^gs8[0-9]$"),
    ("ripening", "senescence", "^gs9[0-9]$"),
    ("ripening", "beginning of dormancy", "^gs9[0-9]$"),
}

group_map = GroupMap()
group_map.add(growth)

print(group_map[1])

f = sys.stdout
f.write("\n")
for image in coco["images"]:
    json.dump({"index": {"_index": "weedid", "_type": "image"}}, f)
    f.write("\n")
    json.dump(image, f)
    f.write("\n")
