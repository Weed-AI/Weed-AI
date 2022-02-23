import argparse
import pathlib
import json
import os
import re
import tempfile
import ocfl
from shutil import copy, move
from zipfile import ZipFile
from PIL import Image
from collections import defaultdict
from weedcoco.utils import get_image_hash, check_if_approved_image_extension
from weedcoco.validation import ValidationError, validate


# image hash calculation methods

def validate_duplicate_images(image_hash):
    if len(get_hashset_from_image_name(image_hash)) != len(image_hash):
        hash_dict = defaultdict(list)
        for image_name, hash_string in image_hash.items():
            hash_dict[hash_string].append(image_name)
        image_pairs = "; ".join(
            [
                " <-> ".join(sorted(hash_dict[hash_string]))
                for hash_string in hash_dict.keys()
                if len(hash_dict[hash_string]) > 1
            ]
        )
        raise ValidationError(
            "There are identical images in the image directory. Identical image sets are: "
            + image_pairs
        )


def validate_existing_images(repository_dir, image_hash):
    addition_hash = get_hashset_from_image_name(image_hash)
    all_existing_hash = get_all_existing_hash(repository_dir)
    if len(all_existing_hash.union(addition_hash)) != len(all_existing_hash) + len(
        addition_hash
    ):
        raise ValidationError("There are identical images in the repository.")


def get_hashset_from_image_name(image_hash):
    return {os.path.splitext(image_name)[0] for image_name in image_hash.values()}


# FIXME - can get all images hashes of the HEAD version of each dataset
# in the repository by fetching the inventories from OCFL
def get_all_existing_hash(repository_dir):
    return {
        os.path.splitext(filename)[0]
        for dirpath, dirnames, filenames in os.walk(repository_dir)
        if os.path.basename(dirpath) == "images"
        for filename in filenames
    }


def create_image_hash(image_dir):
    return {
        image_name: f"{get_image_hash(image_dir / image_name, 16)}{os.path.splitext(image_name)[-1]}"
        for image_name in os.listdir(image_dir)
        if check_if_approved_image_extension(image_name)
    }


def mkdir_safely(local_dir):
    try:
        os.mkdir(local_dir)
    except FileExistsError as e:
        if not local_dir.is_dir():
            raise RuntimeError(f"{local_dir} exists but is not a directory") from e


class RepositoryError(Exception):
    pass


class RepositoryDataset(Object):
    """
    Class representing a dataset to be added to the repository
    """

    def __init__(self, upload_id=None)
        self.upload_id = upload_id_dir

    def validate(self):
        """Called before attempting to deposit."""
        pass


    def build(self, dataset_dir)

def migrate_images(dataset_dir, raw_dir, image_hash):
    image_dir = dataset_dir / "images"
    mkdir_safely(image_dir)
    for image_name_origin in os.listdir(raw_dir):
        if check_if_approved_image_extension(image_name_origin):
            image_path = dataset_dir / "images" / image_hash[image_name_origin]
            if not os.path.isfile(image_path):
                image_origin = Image.open(raw_dir / image_name_origin)
                image_without_exif = Image.new(image_origin.mode, image_origin.size)
                image_without_exif.putdata(image_origin.getdata())
                image_without_exif.save(image_path)


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





class Repository(Object):
    """
    Class representing the repository.

    In 
    """

    def __init__(self, root=None, disposition='pairtree'):
        self.root = root
        self.ocfl = ocfl.Store(root=str(self.root), disposition=disposition)


    def setup_deposit(self, temp_dir, upload_id=None)
        # TODO - the latest_dataset stuff seems to be only used by tests and I'd be
        # happy to take it out
        if not self.root.is_dir:
            self.ocfl.initialize()
        if upload_id is None:
            if not temp_dir.is_dir():
                mkdir_safely(temp_dir)
                deposit_id = "dataset_1"
            else:               
                latest_dataset_dir_index = self.latest_dataset()
                deposit_id = f"dataset_{latest_dataset_dir_index + 1}"
        else:
            deposit_id = upload_id
        dataset_dir = temp_dir / deposit_id
        try:
            os.mkdir(dataset_dir)
        except FileExistsError:
            if upload_id is not None:
                raise
            return setup_dataset_dir(temp_dir, upload_id=None)
        return dataset_dir, deposit_id


    def latest_dataset(self):
        ids = [ op.replace('/', '') for op in self.ocfl.object_paths() ]
        return max(
            [
                int(id.split("_")[-1])
                for id in ids
                if re.fullmatch(r"^dataset_\d+$", id)
            ],
            default=0,
        )


    def deposit(self, upload_id, dataset):
        """dataset is a RepositoryDataset"""
        if not upload_id:
            raise RepositoryError("Can't deposit without an upload_id")
        dataset.validate()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = pathlib.Path(temp_dir)
            ocfl_object_dir = temp_dir / pathlib.Path(upload_id + ".ocfl")
            dataset_dir, deposit_id = self.setup_deposit(temp_dir, upload_id)
            dataset.build(dataset_dir)
            ocfl_object = ocfl.Object(id=upload_id)
            ocfl_object.create(srcdir=dataset_dir, objdir=ocfl_object_dir)
            self.ocfl.add(object_path=ocfl_object_dir) # check atomicity of this
        return str(self.root)



# def atomic_copy(repository_dir, download_dir, temp_dir, deposit_id):
#     dataset_path = temp_dir / deposit_id
#     zip_path = temp_dir / f"{deposit_id}.zip"
#     repository_dir = repository_dir / deposit_id
#     try:
#         if os.path.isfile(zip_path):
#             move(str(zip_path), str(download_dir))
#         if os.path.isdir(dataset_path):
#             move(str(dataset_path), str(repository_dir))
#     except Exception:
#         # roll back to leave a clean repository
#         (download_dir / zip_path).unlink(missing_ok=True)
#         for path in (repository_dir / deposit_id).glob("*"):
#             path.unlink(missing_ok=True)
#         (repository_dir / deposit_id).rmdir()
#         raise


def deposit_orig(weedcoco_path, image_dir, repository_dir, download_dir, upload_id=None):
    image_hash = create_image_hash(image_dir)
    validate_duplicate_images(image_hash)
    validate_existing_images(repository_dir, image_hash)
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = pathlib.Path(temp_dir)
        dataset_dir, deposit_id = setup_dataset_dir(repository_dir, temp_dir, upload_id)
        deposit_weedcoco(weedcoco_path, dataset_dir, image_dir, image_hash)
        migrate_images(dataset_dir, image_dir, image_hash)
        compress_to_download(dataset_dir, deposit_id, temp_dir)
        atomic_copy(repository_dir, download_dir, temp_dir, deposit_id)
    return str(repository_dir)



def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--weedcoco-path", default="cwfid_imageinfo.json", type=pathlib.Path
    )
    ap.add_argument("--image-dir", default="cwfid_images", type=pathlib.Path)
    ap.add_argument("--repository-dir", default="repository", type=pathlib.Path)
    ap.add_argument("--download-dir", default="download", type=pathlib.Path)
    args = ap.parse_args(args)
    repository = Repository(args.repository_dir, args.download_dir)
    dataset = RepoObject(args.weedcoco_path, args.image_dir)
    repository.deposit(dataset)
    # deposit(
    #     args.weedcoco_path,
    #     args.image_dir,
    #     args.repository_dir,
    #     args.download_dir,
    # )


if __name__ == "__main__":
    main()
