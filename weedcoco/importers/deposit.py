import argparse
import pathlib
import json
import os
from shutil import copyfile
from weedcoco.utils import get_image_average_hash


ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--weedcoco-path", default="cwfid_imageinfo.json", type=pathlib.Path)
ap.add_argument("--image-dir", default="cwfid_images", type=pathlib.Path)
ap.add_argument("--repository-dir", default="repository", type=pathlib.Path)
args = ap.parse_args()

with open(args.weedcoco_path) as f:
    weedcoco = json.load(f)

image_hash = {
    image_name: f'{get_image_average_hash(args.image_dir / image_name)}.{image_name.split(".")[-1]}'
    for image_name in os.listdir(args.image_dir)
    if image_name.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"))
}

image_dir = args.repository_dir / "images"
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

for image_origin in os.listdir(args.image_dir):
    image_path = args.repository_dir / ("images/" + image_hash[image_origin])
    if not os.path.isfile(image_path):
        copyfile(args.image_dir / image_origin, image_path)

for image_reference in weedcoco["images"]:
    file_name = image_reference["file_name"].split("/")[-1]
    if file_name in image_hash:
        image_reference["file_name"] = "images/" + image_hash[file_name]

with (args.repository_dir / "weedcoco.json").open("w") as out:
    json.dump(weedcoco, out, indent=4)
