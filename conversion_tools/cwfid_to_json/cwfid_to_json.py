"""
cwfid_to_json.py

Ingests CWFID .yaml annotations and images to produce a WeedCOCO .JSON file.
"""


"""Constants and environment"""

import warnings
import argparse
import yaml
import pathlib
import json
import datetime
from tqdm import tqdm
import os
import PIL.Image

# define paths
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--annotations-dir", default="annotations", type=pathlib.Path)
ap.add_argument("--image-dir", default="cwfid_images", type=pathlib.Path)
ap.add_argument("-o", "--out-path", default="cwfid_imageinfo.json", type=pathlib.Path)
ap.add_argument("--split-path", default=".", type=pathlib.Path)
args = ap.parse_args()


CATEGORY_MAP = {
    # TODO: we need a spec for species unspecified, and we need a spec for species specified
    "crop": {
        "common_name": "carrot",
        "species": "daugus carota",
        "eppo_taxon_code": "DAUCS",
        "eppo_nontaxon_code": "3UMRC",
        "role": "crop",
        "id": 0,
    },
    "weed": {"species": "UNSPECIFIED", "role": "weed", "id": 1},
}


def create_annotations(ann_blob, image_id, starting_idx):
    """
    Function to create annotations annotation yamls
    """
    annotations = []
    for i, obj in enumerate(ann_blob["annotation"], starting_idx):
        category = CATEGORY_MAP[obj["type"]]
        # a COCO polygon is just a sequence [[x1, y1, x2, y2, ...]]
        if not isinstance(obj["points"]["x"], list):
            print(
                f"Found invalid polygon for annotation of {ann_blob['filename']} with points {obj['points']}"
            )
            continue
        polygon = zip(obj["points"]["x"], obj["points"]["y"])
        polygon = sum(polygon, ())  # flatten an iterable of tuples
        polygon = [list(map(int, polygon))]
        # TODO: parse this polygon with pycocotools.frPyObjects(polygon, im_height, im_width)
        # then:
        # * check that mask matches the stored images in cwfid, and that there is not an off-by-one error (due to indexing base)
        # * get area and bbox for annotation object
        annotations.append(
            {
                "id": i,
                "image_id": image_id,
                "category_id": category["id"],
                "segmentation": polygon,
                "iscrowd": 0,
                # something in pycocotools to do this
                # "area": calculate_area(polygon),
                # "bbox": ...
            }
        )
    return annotations


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
    # Calculate resolution in pixels
    resolution = width * height
    return {"width": width, "height": height, "resolution": resolution}


missing_files = []
categories = [CATEGORY_MAP["crop"], CATEGORY_MAP["weed"]]

"""
Create agcontext object.

A list of information necessary to provide appropriate agricultural context.
This information is invariant across a dataset upon upload.

Datasets can be concatenated to include images from multiple different agcontexts.
"""
agcontext = [
    {
        "id": 0,
        "agcontext_name": "cwfid",
        "crop_type": "other",
        "bbch_descriptive_text": "leaf development",
        "bbch_code": "GS10-19",
        "grains_descriptive_text": "seedling",
        "soil_colour": "grey",
        "surface_cover": "none",
        "surface_coverage": "0-25",
        "weather_description": "sunny",
        "location_lat": 53,
        "location_long": 11,
        "location_datum": 4326,
        "upload_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "camera_make": "JAI AD-130GE",
        "camera_lens": "Fujinon TF15-DA-8",
        "camera_lens_focallength": 15,
        "camera_height": 450,
        "camera_angle": 90,
        "camera_fov": 22.6,
        "photography_description": "Mounted on boom",
        "lighting": "natural",
        "cropped_to_plant": False,
        "url": "https://github.com/cwfid/dataset",
    }
]

license = [
    {
        "id": 0,
        "license_name": "CC BY 4.0",
        "license_fullname": "Creative Commons Attribution 4.0",
        "license_version": "4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/",
    }
]
info = [
    {
        "year": 2015,
        "version": 1,
        "description": "YAML annotations and PNG images converted into WeedCOCO",
        "secondary_contributor": "Converted to WeedCOCO by Henry Lydecker",
        "contributor": "Sebastian Haug",
        "id": 0,
    }
]
annotations = []
images = []
progress = tqdm(args.annotations_dir.glob("*_annotation.yaml"))
for ann_path in progress:
    progress.set_description(ann_path.name)
    image_id = int(ann_path.name[:3])
    ann_blob = yaml.safe_load(ann_path.open())

    image = {
        "id": image_id,
        "file_name": os.path.join(args.image_dir, ann_blob["filename"]),
        "license": 0,  # TODO
        "agcontext_id": 0,
    }
    dims = get_image_dimensions(args.image_dir / ann_blob["filename"])

    if dims is None:
        missing_files.append(args.image_dir / ann_blob["filename"])
    else:
        image.update(dims)

    images.append(image)

    annotations.extend(
        create_annotations(ann_blob, image_id, starting_idx=len(annotations))
    )

    collections = [
        # TODO: DCMI conformance
        {
            "author": "Haug, Sebastian and Ostermann, Jörn",
            "title": "A Crop/Weed Field Image Dataset for the Evaluation of Computer Vision Based Precision Agriculture Tasks",
            "year": 2015,
            "identifier": "doi:10.1007/978-3-319-16220-1_8",
            "rights": "All data is subject to copyright and may only be used for non-commercial research. In case of use please cite our publication.",
            "accrual_policy": "Closed",
            "id": 0,
        }
    ]

subset_path = args.split_path / "train_test_split.yaml"
with open(subset_path) as subset_file:
    subsets = yaml.safe_load(subset_file)

    # TODO: iterate over value key pairs and create individual collection membership per image.
    # TODO: refer to all annotations associated with an image?
    collection_memberships = []
    for key, value in subsets.items():
        if key == "train":
            collection_memberships.append(
                {"image_id": value, "subset": "train", "collection_id": 0}
            )
        else:
            collection_memberships.append(
                {"image_id": value, "subset": "test", "collection_id": 0}
            )
print(collection_memberships)
"""Write output"""
with args.out_path.open("w") as fout:
    json.dump(
        {
            "images": images,
            "annotations": annotations,
            "categories": categories,
            "info": info,
            "license": license,
            "agcontexts": agcontext,
            "collections": collections,
            "collection_memberships": collection_memberships,
        },
        fout,
        indent=4,
    )
