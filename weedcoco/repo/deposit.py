import argparse
import pathlib
import json
import os
import re
from shutil import copyfile
from weedcoco.utils import get_image_average_hash
from weedcoco.validation import ValidationError, validate


def validate_duplicate_images(image_hash):
    if len(get_hashset_from_image_name(image_hash)) != len(image_hash):
        raise ValidationError("There are identical images in the image directory.")


def validate_existing_images(repository_dir, image_hash):
    addition_hash = get_hashset_from_image_name(image_hash)
    all_existing_hash = get_all_existing_hash(repository_dir)
    if len(all_existing_hash.union(addition_hash)) != len(all_existing_hash) + len(
        addition_hash
    ):
        raise ValidationError("There are identical images in the repository.")


def get_hashset_from_image_name(image_hash):
    return set(
        map(lambda image_name: os.path.splitext(image_name)[0], image_hash.values())
    )


def get_all_existing_hash(repository_dir):
    return {
        os.path.splitext(filename)[0]
        for dirpath, dirnames, filenames in os.walk(repository_dir)
        if os.path.basename(dirpath) == "images"
        for filename in filenames
    }


def setup_dataset_dir(repository_dir):
    if not os.path.isdir(repository_dir):
        os.mkdir(repository_dir)
        dataset_dir = repository_dir / "dataset_0"
    else:
        latest_dataset_dir_index = max(
            [
                int(dir.split("_")[-1])
                for dir in os.listdir(repository_dir)
                if re.fullmatch(r"^dataset_\d+$", dir)
            ],
            default=0,
        )
        dataset_dir = repository_dir / f"dataset_{latest_dataset_dir_index + 1}"
    os.mkdir(dataset_dir)
    return dataset_dir


def create_image_hash(image_dir):
    return {
        image_name: f"{get_image_average_hash(image_dir / image_name)}{os.path.splitext(image_name)[-1]}"
        for image_name in os.listdir(image_dir)
        if image_name.lower().endswith((".png", ".jpg", ".jpeg", ".tiff"))
    }


def migrate_images(dataset_dir, raw_dir, image_hash):
    image_dir = dataset_dir / "images"
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    for image_origin in os.listdir(raw_dir):
        image_path = dataset_dir / "images" / image_hash[image_origin]
        if not os.path.isfile(image_path):
            copyfile(raw_dir / image_origin, image_path)


def deposit_weedcoco(weedcoco_path, dataset_dir, image_dir, image_hash):
    with open(weedcoco_path) as f:
        weedcoco = json.load(f)
    for image_reference in weedcoco["images"]:
        file_name = image_reference["file_name"].split("/")[-1]
        if file_name in image_hash:
            image_reference["file_name"] = "images/" + image_hash[file_name]

    validate(weedcoco, image_dir)
    with (dataset_dir / "weedcoco.json").open("w") as out:
        json.dump(weedcoco, out, indent=4)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--weedcoco-path", default="cwfid_imageinfo.json", type=pathlib.Path
    )
    ap.add_argument("--image-dir", default="cwfid_images", type=pathlib.Path)
    ap.add_argument("--repository-dir", default="repository", type=pathlib.Path)
    args = ap.parse_args()

    image_hash = create_image_hash(args.image_dir)
    validate_duplicate_images(image_hash)
    validate_existing_images(args.repository_dir, image_hash)

    dataset_dir = setup_dataset_dir(args.repository_dir)
    deposit_weedcoco(args.weedcoco_path, dataset_dir, args.image_dir, image_hash)
    migrate_images(dataset_dir, args.image_dir, image_hash)


if __name__ == "__main__":
    main()
