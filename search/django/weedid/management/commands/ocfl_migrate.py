from django.core.management.base import BaseCommand, CommandError

from weedid.tasks import migrate_to_ocfl
import pathlib
import uuid


class Command(BaseCommand):
    help = "Migrate the contents of a file repository to ocfl"

    def add_arguments(self, parser):
        parser.add_argument("source-dir", type=str)

    def handle(self, *args, **options):
        source_dir = options["source-dir"]
        metadata = {
            "message": "message",
            "address": "admin@weedai.sydney.ed.au",
            "name": "weedAI",
        }
        if not source_dir:
            raise CommandError("No source_dir")
        source_path = pathlib.Path(source_dir)
        if not source_path.is_dir():
            raise CommandError(f"{source_dir} is not a directory")

        for subdir in [x for x in source_path.iterdir() if x.is_dir()]:
            try:
                identifier = str(subdir.name)
                uuid.UUID(identifier)
                self.stdout.write(f"Importing {identifier}")
                migrate_to_ocfl.delay(source_dir, identifier, metadata)
            except ValueError:
                self.stdout.write(f"Skipping non-uuid path {identifier}")
        self.stdout.write("Done")
