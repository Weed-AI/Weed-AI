import re
import tempfile
import logging
import argparse
import pathlib
import ocfl
import uuid

from deposit import Repository, RepositoryError

logger = logging.getLogger(__name__)


def is_valid_version(version):
    if version == "head":
        return True
    if re.match("v[0-9]+$", version):
        return int(version[1:]) > 0


def validate_ocfl(repository, identifier):
    if identifier:
        dataset = repository.dataset(identifier)
        if not dataset.exists_in_repo:
            raise RepositoryError(f"Dataset {identifier} not found in repo")
        dataset.validate()
    else:
        repository.validate()


def list_contents(repository, identifier, version):
    if identifier:
        dataset = repository.dataset(identifier)
        if dataset.exists_in_repo:
            head = int(dataset.head_version[1:])
            if int(version[1:]) > head:
                raise RepositoryError(f"{identifier} has head v{head}")
            for path in dataset.get_logical_paths(version):
                print(path)
        else:
            print(f"Dataset {identifier} not found in repo")
    else:
        for dataset in repository.datasets():
            print(dataset.identifier, dataset.head_version)


def migrate(repository, identifier, src_dir, metadata):
    ocfl_metadata = ocfl.VersionMetadata(
        identifier=identifier,
        message=metadata["message"],
        address=metadata["address"],
        name=metadata["name"],
    )
    dataset = repository.dataset(identifier)
    if dataset.exists_in_repo:
        raise RepositoryError(f"Dataset {identifier} already migrated")
    with tempfile.TemporaryDirectory() as temp_dir:
        new_object_dir = pathlib.Path(temp_dir) / identifier
        new_object = ocfl.Object(identifier=identifier)
        new_object.create(
            objdir=str(new_object_dir),
            srcdir=str(src_dir),
            metadata=ocfl_metadata,
        )
        repository.ocfl.add(object_path=str(new_object_dir))


def migrate_dir(repository, src, metadata):
    for subdir in [x for x in src.iterdir() if x.is_dir()]:
        try:
            identifier = str(subdir.name)
            uuid.UUID(identifier)
            print(f"Importing {identifier}")
            migrate(repository, identifier, subdir, metadata)
        except ValueError:
            print(f"Skipping non-uuid path {identifier}")


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repository-dir", required=True, type=pathlib.Path)
    ap.add_argument("--initialise", default=False, action="store_true")
    ap.add_argument("--identifier", type=str)
    ap.add_argument("--name", default="", type=str)
    ap.add_argument("--address", default="", type=str)
    ap.add_argument("--message", default="", type=str)
    ap.add_argument("--migrate-dir", default=None, type=pathlib.Path)
    ap.add_argument("--migrate", default=None, type=pathlib.Path)
    ap.add_argument("--list", default=False, action="store_true")
    ap.add_argument("--version", default="head", type=str)
    ap.add_argument("--validate", default=False, action="store_true")
    args = ap.parse_args(args)
    metadata = {
        "name": args.name,
        "address": args.address,
        "message": args.message,
    }
    if args.version and not is_valid_version(args.version):
        raise RepositoryError("'{args.version} is not a valid ocfl version")
    repository = Repository(args.repository_dir)
    if args.initialise:
        if args.repository_dir.is_dir():
            raise RepositoryError(
                f"Cannot initalise - {args.repository_dir} already exists"
            )
        print(f"Initialising ocfl repository in {args.repository_dir}")
        return repository.initialize()
    if args.validate:
        return validate_ocfl(repository, args.identifier)
    if args.list:
        return list_contents(repository, args.identifier, args.version)
    if args.migrate_dir:
        return migrate_dir(
            repository,
            args.migrate_dir,
            metadata,
        )
    if args.migrate:
        return migrate(repository, args.identifier, args.migrate, metadata)


if __name__ == "__main__":
    main()
