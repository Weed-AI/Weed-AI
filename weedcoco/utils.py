import json
import os
import warnings

import PIL.Image
import yaml
import imagehash


def get_image_dimensions(path):
    """
    Function to measure image dimensions and calculate resolution.
    """
    if not os.path.isfile(path):
        warnings.warn(f"Could not open {path}")
        return None
    # Retrieve image width and height
    image = PIL.Image.open(path)
    width, height = image.size
    return {"width": width, "height": height}


def load_json_or_yaml(path):
    """Streamlined function for open both JSON and YAML"""
    if path.suffix in (".yml", ".yaml"):
        obj = yaml.safe_load(open(path))
    else:
        obj = json.load(open(path))
    return obj


def add_agcontext_from_file(coco, agcontext_path):
    """Make all images have the same AgContext loaded from YAML or JSON"""
    agcontext = load_json_or_yaml(agcontext_path)
    if "id" not in agcontext:
        agcontext["id"] = 0
    coco["agcontexts"] = [agcontext]
    for image in coco["images"]:
        image["agcontext_id"] = agcontext["id"]
    return coco


def add_collection_from_file(coco, collection_path):
    """Make all annotations members of one collection loaded from YAML or JSON"""
    collection = load_json_or_yaml(collection_path)
    if "id" not in collection:
        collection["id"] = 0
    coco["collections"] = [collection]
    coco["collection_memberships"] = [
        {"annotation_id": annotation["id"], "collection_id": collection["id"]}
        for annotation in coco["annotations"]
    ]
    return coco


def get_image_average_hash(path):
    """Return an average hash of an image"""
    return str(imagehash.average_hash(PIL.Image.open(path), hash_size=16))
