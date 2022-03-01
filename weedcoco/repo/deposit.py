import argparse
import pathlib
import json
import os
import tempfile
import ocfl
from shutil import copy, move, rmtree
from zipfile import ZipFile
from PIL import Image
from collections import defaultdict
from uuid import uuid4
from weedcoco.utils import get_image_hash, check_if_approved_image_extension
from weedcoco.validation import ValidationError, validate


def mkdir_safely(local_dir):
    try:
        os.mkdir(local_dir)
    except FileExistsError as e:
        if not local_dir.is_dir():
            raise RuntimeError(f"{local_dir} exists but is not a directory") from e


def get_hashset_from_image_name(image_hash):
    return {os.path.splitext(image_name)[0] for image_name in image_hash.values()}


class RepositoryError(Exception):
    pass


class RepositoryDataset:
    """
    Class representing a dataset in the ocfl repository
    ---
    repo (Repository): the ocfl repository
    identifier (str): this dataset's unique identifier in the repository
    """

    def __init__(self, repo, identifier):
        self.repo = repo
        self.identifier = identifier
        self.ocfl = None

    def open(self):
        obj_path = self.repo.ocfl.object_path(identifier=self.identifier)
        self.path = self.repo.root / pathlib.Path(obj_path)
        self.ocfl = ocfl.Object(identifier=self.identifier)
        if self.path.is_dir():
            self.ocfl.open_fs(str(self.path))
            return self.path
        else:
            return None

    def sources(self, weedcoco_path, image_dir):
        """Set the weedcoco_path and images_dir for the build"""
        self.weedcoco_path = weedcoco_path
        self.image_dir = image_dir

    def inventory(self):
        """Return the object's inventory"""
        if not self.open():
            raise RepositoryError(f"Object {self.identifier} not found in repository")
        return self.ocfl.parse_inventory()

    def paths(self, version="head"):
        """Iterate over the paths of all the content in a version"""
        inventory = self.inventory()
        if version == "head":
            version = inventory["head"]
        for paths in inventory["versions"][version]["state"].values():
            for path in paths:
                yield path

    def path(self, path, version="head"):
        """Return the actual filesystem path for a logical path in a version."""
        inventory = self.inventory()
        if version == "head":
            version = inventory["head"]
        for digest, paths in inventory["versions"][version]["state"].items():
            if path in paths:
                return inventory["manifest"][digest]
        raise RepositoryError(f"Path {path} not found in version {version}")

    def extract(self, dest_dir, version="head"):
        """
        Write out a version of this object to dest_dir
        """
        if not self.open():
            raise RepositoryError(f"Object {self.identifier} not found in repository")
        self.ocfl.extract(objdir=str(self.path), version=version, dstdir=dest_dir)

    def validate(self, repository):
        """Run checks which need to pass before deposit"""
        self.create_image_hash()
        self.validate_duplicate_images()
        self.validate_existing_images(repository)

    def build(self, dataset_dir):
        """Build a dataset to be deposited"""
        self.write_weedcoco(dataset_dir)
        self.migrate_images(dataset_dir)

    def rollback(self, dataset_dir, last_version):
        """Undo any changes in the event of error. This uses the ocfl object's obj_fs
        for file operations, so that it works on s3 objects as well as traditional fileystems"""
        if last_version:
            inventory = self.inventory()
            if inventory["head"] != last_version:
                vi = int(last_version[1:])
                for version in self.path.glob("v*"):
                    if int(version.name[1:]) > vi:
                        rmtree(str(self.path / version))
                    # self.ocfl.obj_fs.removedir(str(self.path / version), True, True)
                copy(
                    str(self.path / last_version / "inventory.json"),
                    str(self.path / "inventory.json"),
                )
                copy(
                    str(self.path / last_version / "inventory.json.sha512"),
                    str(self.path / "inventory.json.sha512"),
                )
        else:
            # no last_version means a create failed, so remove the whole objext
            if self.path.is_dir():
                rmtree(str(self.path))
                # self.ocfl.open_fs(str(self.path))
                # self.ocfl.obj_fs.removedir(str(self.path), True, True)

    def write_weedcoco(self, dataset_dir):
        with open(self.weedcoco_path) as f:
            weedcoco = json.load(f)
        for image_reference in weedcoco["images"]:
            file_name = image_reference["file_name"].split("/")[-1]
            if file_name in self.image_hash:
                image_reference["file_name"] = "images/" + self.image_hash[file_name]
        validate(weedcoco, self.image_dir)
        new_weedcoco = dataset_dir / "weedcoco.json"
        with (new_weedcoco).open("w") as out:
            json.dump(weedcoco, out, indent=4)

    def migrate_images(self, dataset_dir):
        new_image_dir = dataset_dir / "images"
        mkdir_safely(new_image_dir)
        for image_name_origin in os.listdir(self.image_dir):
            if check_if_approved_image_extension(image_name_origin):
                if image_name_origin in self.image_hash:  # FIXME
                    image_path = new_image_dir / self.image_hash[image_name_origin]
                    if not os.path.isfile(image_path):
                        image_origin = Image.open(self.image_dir / image_name_origin)
                        image_without_exif = Image.new(
                            image_origin.mode, image_origin.size
                        )
                        image_without_exif.putdata(image_origin.getdata())
                        image_without_exif.save(image_path)

    def validate_duplicate_images(self):
        if len(get_hashset_from_image_name(self.image_hash)) != len(self.image_hash):
            hash_dict = defaultdict(list)
            for image_name, hash_string in self.image_hash.items():
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

    def validate_existing_images(self, repository):
        addition_hash = get_hashset_from_image_name(self.image_hash)
        all_existing_hash = self.get_all_existing_hash(repository)
        if len(all_existing_hash.union(addition_hash)) != len(all_existing_hash) + len(
            addition_hash
        ):
            raise ValidationError("There are identical images in the repository.")

    def get_all_existing_hash(self, repository):
        return {
            os.path.splitext(path.split("/")[-1])[0]
            for dataset in repository.datasets()
            if dataset.identifier != self.identifier
            for path in dataset.paths()
            if path.split("/")[0] == "images"
        }

    def create_image_hash(self):
        self.image_hash = {
            image_name: f"{get_image_hash(self.image_dir / image_name, 16)}{os.path.splitext(image_name)[-1]}"
            for image_name in os.listdir(self.image_dir)
            if check_if_approved_image_extension(image_name)
        }

    def retrieve_image_paths(self):
        for root, directories, files in os.walk(self.image_dir):
            for filename in files:
                yield (os.path.join(root, filename), filename)

    def compress_to_download(self, temp_dir):
        mkdir_safely(temp_dir)
        download_path = (temp_dir / self.identifier).with_suffix(".zip")
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = pathlib.Path(tmpdir) / "bundle.zip"
            with ZipFile(zip_path, "w") as zip:
                zip.write(self.weedcoco_path, "weedcoco.json")
                for image, image_name in self.retrieve_image_paths():
                    zip.write(image, "images/" + image_name)
            # XXX: this should be move() not copy(), but move resulted in files
            #      that we could not delete or move in the Docker volume.
            copy(zip_path, download_path)
        return download_path


class Repository:
    """
    Class representing the ocfl repository
    ---
    root (pathlib.Path): the root directory of the repository
    disposition (str): the algorithm used by the ocfl library to map ids to paths
    """

    def __init__(self, root, disposition="pairtree"):
        self.root = root
        self.disposition = disposition
        if self.root.is_dir():
            self.connect()

    def initialize(self):
        if not self.root.is_dir():
            # use a separate ocfl.Store because it will create an invalid
            # ocfl_layout.json if we initialise with a disposition
            ocfl_store = ocfl.Store(root=str(self.root))
            ocfl_store.initialize()

    def connect(self):
        self.ocfl = ocfl.Store(root=str(self.root), disposition=self.disposition)

    def datasets(self):
        self.ocfl.open_root_fs()
        self.ocfl.check_root_structure()
        for path in self.ocfl.object_paths():
            yield RepositoryDataset(self, path.split("/")[-1])

    def dataset(self, identifier):
        dataset = RepositoryDataset(self, identifier)
        if dataset.open():
            return dataset
        else:
            return None

    def setup_deposit(self, temp_dir, deposit_id):
        dataset_dir = temp_dir / deposit_id
        os.mkdir(dataset_dir)
        return dataset_dir

    def deposit(self, identifier, dataset, metadata, download_dir):
        """Validate and deposit a RepositoryDataset in the Repository.  Creates a new
        dataset for identifier if it does not already exist.
        --------
        identifier - the dataset's unique ID. If empty, a uuid is used
        metadata - a dict-like with name, address and message
        dataset - a RepositoryDataset

        Returns the id of the object.
        """
        if not identifier:
            identifier = str(uuid4())
            dataset.identifier = identifier
        else:
            assert "/" not in identifier
        dataset.validate(self)
        ocfl_metadata = ocfl.VersionMetadata(
            identifier=identifier,
            message=metadata["message"],
            address=metadata["address"],
            name=metadata["name"],
        )
        obj_dir = dataset.open()
        last_version = None
        if obj_dir:
            inventory = dataset.inventory()
            last_version = inventory["head"]
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = pathlib.Path(temp_dir)
            dataset_dir = self.setup_deposit(temp_dir, identifier)
            dataset.build(dataset_dir)
            zip_file = dataset.compress_to_download(temp_dir)
            try:
                if obj_dir:
                    dataset.ocfl.update(
                        objdir=str(obj_dir),
                        srcdir=str(dataset_dir),
                        metadata=ocfl_metadata,
                    )
                else:
                    new_object_dir = temp_dir / pathlib.Path(identifier + "_ocfl")
                    new_object = ocfl.Object(identifier=identifier)
                    new_object.create(
                        objdir=str(new_object_dir),
                        srcdir=str(dataset_dir),
                        metadata=ocfl_metadata,
                    )
                    self.ocfl.add(object_path=str(new_object_dir))
                if zip_file.is_file():
                    old_zip = download_dir / zip_file.name
                    if old_zip.is_file():
                        old_zip.unlink()
                    move(str(zip_file), str(download_dir))
            except Exception:
                dataset.rollback(dataset_dir, last_version)
                zip_file = download_dir / zip_file.name
                if zip_file.is_file():
                    zip_file.unlink()  # missing_ok is not in 3.7
                raise
        return dataset


def deposit(
    weedcoco_path, image_dir, repository_dir, download_dir, metadata, upload_id=None
):
    repository = Repository(repository_dir)
    repository.initialize()
    repository.connect()
    dataset = RepositoryDataset(repository, upload_id)
    dataset.sources(weedcoco_path, image_dir)
    repository.deposit(upload_id, dataset, metadata, download_dir)
    return repository, dataset


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--weedcoco-path", default="cwfid_imageinfo.json", type=pathlib.Path
    )
    ap.add_argument("--image-dir", default="cwfid_images", type=pathlib.Path)
    ap.add_argument("--repository-dir", default="repository", type=pathlib.Path)
    ap.add_argument("--download-dir", default="download", type=pathlib.Path)
    ap.add_argument("--identifier", default="", type=str)
    ap.add_argument("--name", default="", type=str)
    ap.add_argument("--address", default="", type=str)
    ap.add_argument("--message", default="", type=str)
    args = ap.parse_args(args)
    repository = Repository(args.repository_dir)
    repository.initialize()
    repository.connect()
    dataset = RepositoryDataset(repository, args.identifier)
    dataset.sources(args.weedcoco_path, args.image_dir)
    metadata = {
        "name": args.name,
        "address": args.address,
        "message": args.message,
    }
    repository.deposit(args.identifier, dataset, metadata, args.download_dir)
    return repository, dataset


if __name__ == "__main__":
    main()
