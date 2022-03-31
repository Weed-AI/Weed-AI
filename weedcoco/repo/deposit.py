import argparse
import hashlib
import json
import logging
import os
import pathlib
import tempfile
from collections import defaultdict
from shutil import copy, move, rmtree
from uuid import uuid4
from zipfile import ZipFile

import ocfl
import redis
from PIL import Image
from weedcoco.utils import check_if_approved_image_extension, get_image_hash
from weedcoco.validation import ValidationError, validate

logger = logging.getLogger(__name__)
COCO_ANNOTATION_FIELD = ("segmentation", "bbox", "area", "iscrowd", "attributes")


def mkdir_safely(local_dir):
    try:
        os.mkdir(local_dir)
    except FileExistsError as e:
        if not local_dir.is_dir():
            raise RuntimeError(f"{local_dir} exists but is not a directory") from e


def get_hashset_from_image_name(image_hash):
    return {os.path.splitext(image_name)[0] for image_name in image_hash.values()}


def retrieve_image_paths(image_dir):
    for root, _, files in os.walk(image_dir):
        for filename in files:
            yield (os.path.join(root, filename), filename)


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

    def update(self, src_dir, metadata):
        self.ocfl.update(
            objdir=str(self.object_path),
            srcdir=str(src_dir),
            metadata=metadata,
        )
        self._inventory = self.ocfl.parse_inventory()

    def validate(self):
        self.ocfl.validate(str(self.object_path))

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

    def validate_image(self):
        """Run checks which need to pass before deposit"""
        self.validate_duplicate_images()
        self.validate_existing_images()

    def set_sources(self, weedcoco_path, image_dir):
        """Set the weedcoco_path and images_dir for the build"""
        self.weedcoco_path = weedcoco_path
        self.image_dir = image_dir
        self.create_image_hash_and_mapping()

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
        reverse_mapping = {
            value.split(".")[0]: key for key, value in self.image_hash.items()
        }
        for hash_name in addition_hash:
            if (
                hash_name in all_existing_hash
                and all_existing_hash[hash_name] != self.identifier
            ):
                raise ValidationError(
                    "There are identical images in the repository. Existing image hash names are: "
                    + "; ".join(
                        [
                            " <-> ".join(
                                [
                                    f"{self.identifier}/{reverse_mapping[existing_hash]}",
                                    f"{all_existing_hash[existing_hash]}/{existing_hash}",
                                ]
                            )
                            for existing_hash in addition_hash
                            & set(all_existing_hash.keys())
                        ]
                    )
                )

    def get_all_existing_hash(self, repository):
        return {
            os.path.splitext(path.split("/")[-1])[0]: dataset.identifier
            for dataset in repository.datasets()
            if dataset.identifier != self.identifier
            for path in dataset.get_logical_paths()
            if path.split("/")[0] == "images"
        }

    def create_image_hash_and_mapping(self):
        annotations_hash = self.create_annotation_hash()
        self.create_image_hash(annotations_hash)

    def create_annotation_hash(self):
        annotations_hash = defaultdict(str)
        with open(self.weedcoco_path) as f:
            weedcoco = json.load(f)
        image_id_mapping = {
            image["id"]: image["file_name"].split("/")[-1]
            for image in weedcoco["images"]
        }
        image_annotation_mapping = {
            image_id_mapping[annotation["image_id"]]: {
                key: value
                for key, value in annotation.items()
                if key in COCO_ANNOTATION_FIELD
            }
            for annotation in weedcoco["annotations"]
        }
        for image_name, image_annotation in image_annotation_mapping.items():
            annotations_hash[image_name] = hashlib.md5(
                json.dumps(image_annotation, sort_keys=True).encode("utf-8")
            ).hexdigest()
        return annotations_hash

    def create_image_hash(self, annotations_hash):
        self.image_hash = {
            image_name: f"{get_image_hash(self.image_dir / image_name, 16)}-{annotations_hash[image_name]}{os.path.splitext(image_name)[-1]}"
            for image_name in os.listdir(self.image_dir)
            if check_if_approved_image_extension(image_name)
        }

    def store_image_hash_mapping(self, redis_url):
        redis_client = redis.Redis.from_url(url=redis_url)
        for image_name, image_hash in self.image_hash.items():
            redis_client.set("/".join([self.identifier, image_hash]), image_name)

    def extract_original_images(self, dest_dir, redis_mapping_url="", version="head"):
        """
        Checks out a version of a dataset from the ocfl repository and then
        tries to remap the image filenames to their originals, also updating the
        weedcoco. If the images have no redis mappings, leaves them unchanged.
        """
        redis_client = (
            redis.Redis.from_url(url=redis_mapping_url) if redis_mapping_url else None
        )
        if not self.exists_in_repo:
            raise RepositoryError("dataset not found")
        if os.path.isdir(dest_dir):
            rmtree(dest_dir)
        self.extract(dest_dir, version)
        if redis_client:
            logger.warning(f"remapping images for {version} of {self.identifier}")
            weedcoco_path = os.path.join(dest_dir, "weedcoco.json")
            with open(weedcoco_path, "r") as jsonFile:
                weedcoco_json = json.load(jsonFile)
            images_path = os.path.join(dest_dir, "images")
            images_set = set(os.listdir(images_path))
            for hash_image in images_set:
                redis_key = "/".join([self.identifier, hash_image])
                original_image = redis_client.get(
                    "/".join([self.identifier, hash_image])
                )
                logger.warning(f"<REDIS> {redis_key} maps to {original_image}")
                if original_image:
                    move(
                        os.path.join(images_path, hash_image),
                        os.path.join(images_path, original_image.decode("ascii")),
                    )
                else:
                    logger.warning(f"No match found for {redis_key}")
            for image in weedcoco_json["images"]:
                hash_name = image["file_name"].split("/")[-1]
                original_image = redis_client.get(
                    "/".join([self.identifier, hash_name])
                )
                if hash_name in images_set and original_image:
                    image["file_name"] = original_image.decode("ascii")
            with open(weedcoco_path, "w") as jsonFile:
                jsonFile.write(json.dumps(weedcoco_json, indent=4))

    def make_zipfile(self, download_dir, redis_url=None, version="head"):
        zip_file = (download_dir / self.identifier).with_suffix(".zip")
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_zip = pathlib.Path(tmpdir) / "bundle.zip"
            tmp_dest = pathlib.Path(tmpdir) / self.identifier
            self.extract_original_images(tmp_dest, redis_url)
            with ZipFile(tmp_zip, "w") as zip:
                zip.write(tmp_dest / "weedcoco.json", "weedcoco.json")
                for image, image_name in retrieve_image_paths(tmp_dest / "images"):
                    zip.write(image, "images/" + image_name)
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

    def validate(self):
        self.ocfl.validate()

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

    def deposit(self, identifier, dataset, metadata, download_dir, redis_url=None):
        """Validate and deposit a RepositoryDataset in the Repository.  Creates a new
        dataset for identifier if it does not already exist.
        --------
        identifier - the dataset's unique ID. If empty, a uuid is used
        metadata - a dict-like with name, address and message
        dataset - a RepositoryDataset

        Returns the updated dataset
        """
        if identifier is None:
            identifier = str(uuid4())
            dataset.identifier = identifier
        else:
            assert "/" not in identifier
        dataset.validate_image()
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
            head_zipfile = (download_dir / identifier).with_suffix(".zip")
            last_zipfile = (download_dir / identifier).with_suffix(
                f".{last_version}.zip"
            )
            try:
                if dataset.exists_in_repo:
                    dataset.update(dataset_dir, ocfl_metadata)
                    logger.warning(f"copying {head_zipfile} to {last_zipfile}")
                    copy(head_zipfile, last_zipfile)
                else:
                    new_object_dir = temp_dir / pathlib.Path(identifier + "_ocfl")
                    new_object = ocfl.Object(identifier=identifier)
                    new_object.create(
                        objdir=str(new_object_dir),
                        srcdir=str(dataset_dir),
                        metadata=ocfl_metadata,
                    )
                    self.ocfl.add(object_path=str(new_object_dir))
                dataset.make_zipfile(download_dir, redis_url)
            except Exception:
                dataset.rollback(dataset_dir, last_version)
                if head_zipfile.is_file():
                    head_zipfile.unlink()  # missing_ok is not in 3.7
                if last_version != "v1":
                    move(last_zipfile, head_zipfile)
                raise
        return dataset


def deposit(
    weedcoco_path,
    image_dir,
    repository_dir,
    download_dir,
    metadata,
    upload_id=None,
    redis_url=None,
):
    repository = Repository(repository_dir)
    repository.initialize()
    dataset = repository.dataset(upload_id)
    dataset.set_sources(weedcoco_path, image_dir)
    if redis_url:
        dataset.store_image_hash_mapping(redis_url)
    repository.deposit(upload_id, dataset, metadata, download_dir, redis_url)
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
