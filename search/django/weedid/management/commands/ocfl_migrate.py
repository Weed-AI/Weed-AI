from django.core.management.base import BaseCommand, CommandError

from weedid.tasks import migrate_ocfl_all
import pathlib

from core.settings import REPOSITORY_DIR


class Command(BaseCommand):
    help = "Migrate the contents of a file repository to ocfl"

    def add_arguments(self, parser):
        parser.add_argument("source", type=str)

    def handle(self, *args, **options):
        source_dir = options["source"]
        metadata = {
            "message": "message",
            "address": "admin@weedai.sydney.ed.au",
            "name": "weedAI",
        }
        if source_dir:
            if not pathlib.Path(source_dir).is_dir():
                raise CommandError(f"{source_dir} is not a directory")
            migrate_ocfl_all.delay(source_dir, metadata, REPOSITORY_DIR)
