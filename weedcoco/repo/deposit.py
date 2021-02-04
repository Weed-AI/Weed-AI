import argparse
import pathlib
import json
import os
import re
import tempfile
from shutil import copyfile, copy
from zipfile import ZipFile
from weedcoco.utils import get_image_average_hash, check_if_approved_image_extension
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
    return {os.path.splitext(image_name)[0] for image_name in image_hash.values()}


def get_all_existing_hash(repository_dir):
    return {
        os.path.splitext(filename)[0]
        for dirpath, dirnames, filenames in os.walk(repository_dir)
        if os.path.basename(dirpath) == "images"
        for filename in filenames
    }


def mkdir_safely(local_dir):
    try:
        os.mkdir(local_dir)
    except FileExistsError as e:
        if not local_dir.is_dir():
            raise RuntimeError(f"{local_dir} exists but is not a directory") from e


def setup_dataset_dir(repository_dir, upload_id=None):
    if upload_id is None:
        if not repository_dir.is_dir():
            mkdir_safely(repository_dir)
            deposit_id = "dataset_1"
        else:
            latest_dataset_dir_index = max(
                [
                    int(dir.split("_")[-1])
                    for dir in os.listdir(repository_dir)
                    if re.fullmatch(r"^dataset_\d+$", dir)
                ],
                default=0,
            )
            deposit_id = f"dataset_{latest_dataset_dir_index + 1}"
    else:
        deposit_id = upload_id
    dataset_dir = repository_dir / deposit_id
    try:
        os.mkdir(dataset_dir)
    except FileExistsError:
        if upload_id is not None:
            raise
        return setup_dataset_dir(repository_dir, upload_id=None)
    return dataset_dir, deposit_id


def create_image_hash(image_dir):
    return {
        image_name: f"{get_image_average_hash(image_dir / image_name, 10)}{os.path.splitext(image_name)[-1]}"
        for image_name in os.listdir(image_dir)
        if check_if_approved_image_extension(image_name)
    }


def migrate_images(dataset_dir, raw_dir, image_hash):
    image_dir = dataset_dir / "images"
    mkdir_safely(image_dir)
    for image_origin in os.listdir(raw_dir):
        if check_if_approved_image_extension(image_origin):
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
    new_dataset_dir = dataset_dir / "weedcoco.json"
    with (new_dataset_dir).open("w") as out:
        json.dump(weedcoco, out, indent=4)
    return new_dataset_dir


def retrieve_image_paths(images_path):
    for root, directories, files in os.walk(images_path):
        for filename in files:
            yield (os.path.join(root, filename), filename)


def compress_to_download(dataset_dir, deposit_id, download_dir):
    mkdir_safely(download_dir)
    download_path = (download_dir / deposit_id).with_suffix(".zip")
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = pathlib.Path(tmpdir) / "bundle.zip"
        with ZipFile(zip_path, "w") as zip:
            zip.write(dataset_dir / "weedcoco.json", "weedcoco.json")
            for image, image_name in retrieve_image_paths(dataset_dir / "images"):
                zip.write(image, "images/" + image_name)
        # XXX: this should be move() not copy(), but move resulted in files
        #      that we could not delete or move in the Docker volume.
        copy(zip_path, download_path)  


def deposit(weedcoco_path, image_dir, repository_dir, download_dir, upload_id=None):
    image_hash = create_image_hash(image_dir)
    validate_duplicate_images(image_hash)
    validate_existing_images(repository_dir, image_hash)
    dataset_dir, deposit_id = setup_dataset_dir(repository_dir, upload_id)
    new_dataset_dir = deposit_weedcoco(
        weedcoco_path, dataset_dir, image_dir, image_hash
    )
    migrate_images(dataset_dir, image_dir, image_hash)
    compress_to_download(dataset_dir, deposit_id, download_dir)
    return str(new_dataset_dir)


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--weedcoco-path", default="cwfid_imageinfo.json", type=pathlib.Path
    )
    ap.add_argument("--image-dir", default="cwfid_images", type=pathlib.Path)
    ap.add_argument("--repository-dir", default="repository", type=pathlib.Path)
    ap.add_argument("--download-dir", default="download", type=pathlib.Path)
    args = ap.parse_args(args)
    deposit(args.weedcoco_path, args.image_dir, args.repository_dir, args.download_dir)


if __name__ == "__main__":
    main()
