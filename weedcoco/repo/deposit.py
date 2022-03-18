import argparse
import pathlib
import json
import os
import tempfile
import ocfl
from shutil import copy, rmtree
from zipfile import ZipFile
from PIL import Image
from collections import defaultdict
from uuid import uuid4
from weedcoco.utils import get_image_hash, check_if_approved_image_extension
from weedcoco.validation import ValidationError, validate

import logging

logger = logging.getLogger(__name__)


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
        self._ocfl = None
        self._inventory = None
        self._object_path = None

    @property
    def ocfl(self):
        if self._ocfl is not None:
            return self._ocfl
        rel_path = self.repo.ocfl.object_path(identifier=self.identifier)
        self._object_path = self.repo.root / pathlib.Path(rel_path)
        if self._object_path.is_dir():
            self._ocfl = ocfl.Object(identifier=self.identifier)
            self._ocfl.open_fs(str(self._object_path))
            return self._ocfl
        else:
            return None

    @property
    def object_path(self):
        """
        Returns a pathlib.Path to the dataset's OCFL object, or None if
        an object with this identifier isn't found in the repo
        """
        if self._object_path is not None:
            return self._object_path
        if self.ocfl is not None:
            return self._object_path
        return None

    @property
    def exists_in_repo(self):
        if self.ocfl is not None:
            return True
        return False

    @property
    def inventory(self):
        """The object's parsed inventory."""
        if self._inventory is not None:
            return self._inventory
        if self.ocfl is not None:
            self._inventory = self.ocfl.parse_inventory()
            return self._inventory
        return None

    @property
    def head_version(self):
        if self.inventory is not None:
            return self._inventory["head"]
        return None

    def get_logical_paths(self, version="head"):
        """Iterate over all content in a version as logical paths"""
        if self.inventory is None:
            raise RepositoryError(f"Object {self.identifier} not in repository")
        if version == "head":
            version = self.inventory["head"]
        for paths in self.inventory["versions"][version]["state"].values():
            for path in paths:
                yield path

    def resolve_path(self, logical_path, version="head"):
        if self.inventory is None:
            raise RepositoryError(f"Object {self.identifier} not in repository")
        if version == "head":
            version = self.inventory["head"]
        for digest, paths in self.inventory["versions"][version]["state"].items():
            if logical_path in paths:
                return self.object_path / pathlib.Path(
                    self.inventory["manifest"][digest][0]
                )
        raise RepositoryError(
            f"Logical path {logical_path} not found in version {version}"
        )

    def extract(self, dest_dir, version="head"):
        """Write out a version of this object to dest_dir"""
        if not self.exists_in_repo:
            raise RepositoryError(f"Object {self.identifier} not found in repository")
        self.ocfl.extract(
            objdir=str(self.object_path), version=version, dstdir=dest_dir
        )

    def validate(self):
        """Run checks which need to pass before deposit"""
        self.create_image_hash()
        self.validate_duplicate_images()
        self.validate_existing_images()

    def set_sources(self, weedcoco_path, image_dir):
        """Set the weedcoco_path and images_dir for the build"""
        self.weedcoco_path = weedcoco_path
        self.image_dir = image_dir

    def build(self, dataset_dir):
        """Build a dataset to be deposited"""
        self.write_weedcoco(dataset_dir)
        self.migrate_images(dataset_dir)

    def rollback(self, dataset_dir, last_version):
        """Undo any changes in the event of error.
        TODO: should use the ocfl's filesystem object so that it works on other
        forms of storage like s3"""
        if last_version:
            if self.inventory["head"] != last_version:
                version_number = int(last_version[1:])
                for version in self.object_path.glob("v*"):
                    if int(version.name[1:]) > version_number:
                        rmtree(str(self.object_path / version))
                copy(
                    str(self.object_path / last_version / "inventory.json"),
                    str(self.object_path / "inventory.json"),
                )
                copy(
                    str(self.object_path / last_version / "inventory.json.sha512"),
                    str(self.object_path / "inventory.json.sha512"),
                )
        else:
            # no last_version means a create failed, so remove the whole object
            if self.object_path.is_dir():
                rmtree(str(self.object_path))

    def write_weedcoco(self, dataset_dir):
        with open(self.weedcoco_path) as f:
            weedcoco = json.load(f)
        for image_reference in weedcoco["images"]:
            file_name = image_reference["file_name"].split("/")[-1]
            if file_name in self.image_hash:
                image_reference["file_name"] = "images/" + self.image_hash[file_name]
        validate(weedcoco, self.image_dir)
        new_weedcoco = dataset_dir / "weedcoco.json"
        with new_weedcoco.open("w") as out:
            json.dump(weedcoco, out, indent=4)

    def migrate_images(self, dataset_dir):
        new_image_dir = dataset_dir / "images"
        mkdir_safely(new_image_dir)
        for image_name_origin in os.listdir(self.image_dir):
            if check_if_approved_image_extension(image_name_origin):
                if image_name_origin in self.image_hash:  # FIXME
                    logger.info(
                        f"Renaming original image {image_name_origin} -> {self.image_hash[image_name_origin]}"
                    )
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

    def validate_existing_images(self):
        addition_hash = get_hashset_from_image_name(self.image_hash)
        all_existing_hash = self.get_all_existing_hash(self.repo)
        if len(all_existing_hash.union(addition_hash)) != len(all_existing_hash) + len(
            addition_hash
        ):
            raise ValidationError("There are identical images in the repository.")

    def get_all_existing_hash(self, repository):
        return {
            os.path.splitext(path.split("/")[-1])[0]
            for dataset in repository.datasets()
            if dataset.identifier != self.identifier
            for path in dataset.get_logical_paths()
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

    def make_zipfile(self, download_dir, version="head"):
        zip_file = (download_dir / self.identifier).with_suffix(".zip")
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_zip = pathlib.Path(tmpdir) / "bundle.zip"
            with ZipFile(tmp_zip, "w") as zip:
                for lpath in self.get_logical_paths(version):
                    zip.write(self.resolve_path(lpath), lpath)
            # XXX: this should be move() not copy(), but move resulted in files
            #      that we could not delete or move in the Docker volume.
            # copy(tmp_zip_path, download_path)
            if tmp_zip.is_file():
                if zip_file.is_file():
                    zip_file.unlink()
                copy(str(tmp_zip), str(zip_file))


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
        self._ocfl = None

    # this requires the ocfl root to not exist (because the OCFL libary won't
    # create a new root in an existing directory)
    def initialize(self):
        if not self.root.is_dir():
            # use a separate ocfl.Store because it will create an invalid
            # ocfl_layout.json if we initialise with a disposition
            ocfl_store = ocfl.Store(root=str(self.root))
            ocfl_store.initialize()

    @property
    def ocfl(self):
        if self._ocfl is not None:
            return self._ocfl
        self._ocfl = ocfl.Store(root=str(self.root), disposition=self.disposition)
        return self._ocfl

    def datasets(self):
        self.ocfl.open_root_fs()
        self.ocfl.check_root_structure()
        for path in self.ocfl.object_paths():
            yield RepositoryDataset(self, path.split("/")[-1])

    def dataset(self, identifier):
        return RepositoryDataset(self, identifier)

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
        if identifier is None:
            identifier = str(uuid4())
            dataset.identifier = identifier
        else:
            assert "/" not in identifier
        dataset.validate()
        ocfl_metadata = ocfl.VersionMetadata(
            identifier=identifier,
            message=metadata["message"],
            address=metadata["address"],
            name=metadata["name"],
        )
        last_version = dataset.head_version
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = pathlib.Path(temp_dir)
            dataset_dir = self.setup_deposit(temp_dir, identifier)
            dataset.build(dataset_dir)
            try:
                if dataset.exists_in_repo:
                    dataset.ocfl.update(
                        objdir=str(dataset.object_path),
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
                dataset.make_zipfile(download_dir)  # should this raise an exception?
            except Exception:
                dataset.rollback(dataset_dir, last_version)
                zip_file = (download_dir / self.identifier).with_suffix(".zip")
                if zip_file.is_file():
                    zip_file.unlink()  # missing_ok is not in 3.7
                raise
        return dataset


def deposit(
    weedcoco_path, image_dir, repository_dir, download_dir, metadata, upload_id=None
):
    repository = Repository(repository_dir)
    repository.initialize()
    dataset = repository.dataset(upload_id)
    dataset.set_sources(weedcoco_path, image_dir)
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
    metadata = {
        "name": args.name,
        "address": args.address,
        "message": args.message,
    }
    return deposit(
        args.weedcoco_path,
        args.image_dir,
        args.repository_dir,
        args.download_dir,
        metadata,
        args.identifier,
    )


if __name__ == "__main__":
    main()
