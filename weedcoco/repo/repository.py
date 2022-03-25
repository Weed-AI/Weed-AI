import re
import tempfile
import logging
import argparse
import pathlib
import ocfl

from deposit import Repository, RepositoryError

logger = logging.getLogger(__name__)


def is_valid_version(version):
    if version == "head":
        return True
    if re.match("v[0-9]+$", version):
        return int(version[1:]) > 0


def validate_ocfl(repository, identifier):
    pass


def list_contents(repository, identifier, version):
    if identifier:
        dataset = repository.dataset(identifier)
        if dataset.exists_in_repo:
            head = int(dataset.head_version[1:])
            if int(version[1:]) > head:
                raise RepositoryError(f"Lastest version of {identifier} is v{head}")
            for path in dataset.get_logical_paths(version):
                print(path)
        else:
            print(f"Dataset {identifier} not found in repo")
    else:
        for dataset in repository.datasets():
            print(dataset.identifier, dataset.head_version)


def migrate(repository, identifier, src, dry_run, metadata):
    ocfl_metadata = ocfl.VersionMetadata(
        identifier=identifier,
        message=metadata["message"],
        address=metadata["address"],
        name=metadata["name"],
    )
    dataset = repository.dataset(identifier)
    if dataset.exists_in_repo:
        if dry_run:
            new_version = int(dataset.head_version[1:]) + 1
            print(f"Dataset {identifier} will be updated to v{new_version}")
            return None
        dataset.update(src, ocfl_metadata)
        return dataset.head_version
    else:
        if dry_run:
            print(f"Dataset {identifier} will be created at v1")
            return None
        with tempfile.TemporaryDirectory() as temp_dir:
            new_object_dir = pathlib.Path(temp_dir) / identifier
            new_object = ocfl.Object(identifier=identifier)
            new_object.create(
                objdir=str(new_object_dir),
                srcdir=str(src),
                metadata=ocfl_metadata,
            )
            repository.ocfl.add(object_path=str(new_object_dir))
        return "v1"


def migrate_dir(repository, src, dry_run, metadata):
    for subdir in [x for x in src.iterdir() if x.is_dir()]:
        migrate(repository, str(subdir), subdir, dry_run, metadata)


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repository-dir", default="repository", type=pathlib.Path)
    ap.add_argument("--identifier", default="", type=str)
    ap.add_argument("--name", default="", type=str)
    ap.add_argument("--address", default="", type=str)
    ap.add_argument("--message", default="", type=str)
    ap.add_argument("--migrate-dir", default=None, type=pathlib.Path)
    ap.add_argument("--migrate", default=None, type=pathlib.Path)
    ap.add_argument("--dry-run", default=False, action="store_true")
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
    if args.validate:
        return validate_ocfl(repository, args.identifier)
    if args.list:
        return list_contents(repository, args.identifier, args.version)
    if args.migrate_dir:
        return migrate_dir(
            repository,
            args.migrate_dir,
            args.dry_run,
            metadata,
        )
    if args.migrate:
        return migrate(
            repository, args.identifier, args.migrate, args.dry_run, metadata
        )


if __name__ == "__main__":
    main()
