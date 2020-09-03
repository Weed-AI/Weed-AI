#!/usr/bin/env python
# coding: utf-8
# Exports Weed COCO on stdin to ElasticSearch _bulk data on stdout

import sys
import json
import logging

log = logging.getLogger()
logging.basicConfig(level=logging.INFO)


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


f = sys.stdout
f.write("\n")
for image in coco["images"]:
    json.dump({"index": {"_index": "weedid", "_type": "image"}}, f)
    f.write("\n")
    json.dump(image, f)
    f.write("\n")
