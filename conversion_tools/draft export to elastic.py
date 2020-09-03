#!/usr/bin/env python
# coding: utf-8
# Exports Weed COCO on stdin to ElasticSearch _bulk data on stdout

import sys
import json
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument('--thumbnail-dir', help='Replace the input file_name directory with this')
args = ap.parse_args()

coco = json.load(sys.stdin)
del coco["info"]
try:
    del coco["collection_memberships"]
except KeyError:
    pass


id_lookup = {}
for key, objs in coco.items():
    for obj in objs:
        id_lookup[key, obj["id"]] = obj


for agcontext in coco["agcontexts"]:
    # massage for ES
    if agcontext.get("camera_fov") == "variable":
        del agcontext["camera_fov"]

for annotation in coco["annotations"]:
    image = id_lookup["images", annotation["image_id"]]
    image.setdefault("annotations", []).append(annotation)
    annotation["category"] = id_lookup["categories", annotation["category_id"]]
    if "agcontext_id" in annotation:
        # Handle legacy version where agcontext_id appears in annotation
        annotation["agcontext"] = id_lookup["agcontexts", annotation["agcontext_id"]]
    else:
        annotation["agcontext"] = id_lookup["agcontexts", image["agcontext_id"]]
    # todo: add collection, license
    if hasattr(args, 'thumbnail_dir'):
        image['thumbnail'] = args.thumbnail_dir + '/' + os.path.basename(image['file_name'])
    else:
        image['thumbnail'] = image['file_name']


f = sys.stdout
f.write("\n")
for image in coco["images"]:
    json.dump({"index": {"_index": "weedid", "_type": "image"}}, f)
    f.write("\n")
    json.dump(image, f)
    f.write("\n")
