import hashlib
import json
import os
import pathlib
import re
import warnings

import imagehash
import joblib
import PIL.Image
import PIL.ImageOps
import requests
import yaml

memory = joblib.Memory(pathlib.Path(__file__).parent / "_cache")


def set_info(coco, metadata):
    info = coco.get("info", {}).copy()
    info["metadata"] = metadata
    info["description"] = metadata["name"]
    try:
        info["year"] = int(metadata["datePublished"][:4])
    except Exception:
        pass
    coco["info"] = info


def set_licenses(coco, metadata=None):
    """Set the license for each image to be that from the metadata"""
    if metadata is None:
        metadata = coco["info"]["metadata"]
    coco["licenses"] = [{"id": 0, "url": metadata["license"]}]
    for image in coco["images"]:
        image["license"] = 0


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
    with open(path) as f:
        if path.suffix in (".yml", ".yaml"):
            obj = yaml.safe_load(f)
        else:
            obj = json.load(f)
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


def add_metadata_from_file(coco, metadata_path):
    """Load metadata from YAML or JSON to set info and licenses"""
    metadata = load_json_or_yaml(metadata_path)
    set_info(coco, metadata)
    set_licenses(coco)
    return coco


def get_image_hash(path, image_hash_size=8, digest_size=20):
    """Return an average hash of an image, rehashed to compress it"""
    md5 = hashlib.md5()
    img_hash = str(
        imagehash.average_hash(PIL.Image.open(path), hash_size=image_hash_size)
    )
    md5.update(img_hash.encode("utf8"))
    return md5.hexdigest()[:digest_size]


def check_if_approved_image_extension(image_name):
    return image_name.lower().endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff"))


def check_if_approved_image_format(image_ext):
    return image_ext in ("PNG", "JPG", "JPEG", "TIFF", "MPO")


def copy_without_exif(src, dest):
    """Makes a copy of an image with any exif metadata stripped out.
    Before copying, uses exif_transpose to orient the image correctly
    if it has an exif orientation value != 1."""
    image_origin = PIL.ImageOps.exif_transpose(PIL.Image.open(src))
    image_without_exif = PIL.Image.new(image_origin.mode, image_origin.size)
    image_without_exif.putdata(image_origin.getdata())
    image_without_exif.save(dest)


def _get_growth_stage_names():
    global __GROWTH_STAGE_NAMES
    try:
        return __GROWTH_STAGE_NAMES
    except NameError:
        pass
    data_path = pathlib.Path(__file__).parent / "growth_stage_labels.json"
    data = json.load(open(data_path))
    out = {}
    # JSON requires string keys
    out["fine"] = {int(k): v for k, v in data.pop("fine").items()}
    for scheme, ranges in data.items():
        out[scheme] = {}
        for range_ in ranges:
            for i in range(range_["lo"], range_["hi"] + 1):
                out[scheme][i] = range_["label"]
    __GROWTH_STAGE_NAMES = out
    return out


def lookup_growth_stage_name(idx, scheme):
    valid = ["fine", "bbch_ranges", "grain_ranges"]
    if scheme not in valid:
        raise ValueError(f"scheme must be one of {valid}. Got {scheme}")
    return _get_growth_stage_names()[scheme][idx]


def get_task_types(annotations):
    if not annotations:
        return set()
    if hasattr(annotations, "items"):
        annotations = [annotations]
    out = {"classification"}
    for annotation in annotations:
        if annotation.get("segmentation"):  # empty segmentation should not be counted
            out.add("segmentation")
            # FIXME: should we be assuming that one should turn segmentation into bbox?
            out.add("bounding box")
        if "bbox" in annotation:
            out.add("bounding box")
    return out


def parse_category_name(name):
    match = re.fullmatch(r"(crop|weed|none)(?:: ([^(]+))?(?: \((.*)\))?", name)
    if match:
        return {
            "name": name,
            "role": match.group(1),
            "taxon": match.group(2),
            "subcategory": match.group(3),
        }


def format_category_name(role, taxon=None, subcategory=None):
    out = role
    if taxon:
        out += f": {taxon}"
    if subcategory:
        out += f" ({subcategory})"
    return out


@memory.cache
def get_gbif_record(canonical_name):
    results = requests.get(
        "https://api.gbif.org/v1/species",
        params={
            "name": canonical_name,
            "datasetKey": "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c",
        },
    ).json()
    # assert results["endOfRecords"]  # TODO?: pagination
    try:
        gbif_record = next(
            record
            for record in results["results"]
            if record["canonicalName"].lower() == canonical_name.lower()
            and record["taxonomicStatus"] == "ACCEPTED"
        )
    except StopIteration:
        raise ValueError(f"No accepted GBIF entries for {repr(canonical_name)}")
    return gbif_record


def get_supercategory_names(name):
    if not name.startswith("weed: "):
        return []

    taxon = name.split(": ", 1)[1]
    if len(taxon.split(" (")) > 1:
        out = ["weed", name, name.split(" (")[0]]
        taxon = taxon.split(" (")[0]
    else:
        out = ["weed"]
    if taxon == "UNSPECIFIED":
        return out

    try:
        record = get_gbif_record(taxon)
    except ValueError:
        warnings.warn(f"Failed to lookup species/taxon {repr(taxon)}")
        return out

    ancestors = {
        rank: record[rank]
        for rank in ["kingdom", "phylum", "order", "family", "genus", "species"]
        if rank in record
    }
    family = ancestors.get("family", None)
    if family != "Poaceae":
        out.append("weed: non-poaceae")

    if family is not None:
        out.append(f"weed: {family.lower()}")
    return out


def denormalise_weedcoco(weedcoco):
    """Puts objects into images from ID references

    E.g. "annotations" added to images and "category" to annotations

    Operates in-place.
    """
    id_lookup = {}
    for key, objs in weedcoco.items():
        for obj in objs:
            if "id" in obj:
                id_lookup[key, obj["id"]] = obj

    for annotation in weedcoco["annotations"]:
        image = id_lookup["images", annotation["image_id"]]
        image.setdefault("annotations", []).append(annotation)
        annotation["category"] = id_lookup["categories", annotation["category_id"]]

    for image in weedcoco["images"]:
        if "agcontext_id" in image:
            image["agcontext"] = id_lookup["agcontexts", image["agcontext_id"]]


def fix_compatibility_quirks(weedcoco):
    """Fix minor issues for compatibility with other COCO tools. Operates in-place"""
    for ann in weedcoco["annotations"]:
        if "bbox" in ann and "segmentation" not in ann:
            ann["segmentation"] = []
