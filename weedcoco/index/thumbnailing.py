import argparse
import os
import pathlib
from PIL import Image
from weedcoco.utils import (
    check_if_approved_image_format,
    check_if_approved_image_extension,
)


def thumbnailing(thumbnails_dir, repository_dir, THUMBNAIL_SIZE=(300, 300)):
    for dirpath, dirnames, filenames in os.walk(repository_dir):
        for filename in filenames:
            if check_if_approved_image_extension(filename):
                image_path = thumbnails_dir / filename[:2] / filename
                if not image_path.is_file():
                    image = Image.open(f"{dirpath}/{filename}")
                    if check_if_approved_image_format(image.format):
                        image.thumbnail(THUMBNAIL_SIZE)
                        if filename[:2] not in os.listdir(thumbnails_dir):
                            os.mkdir(thumbnails_dir / filename[:2])
                        image.save(image_path)


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--thumbnails-dir", type=pathlib.Path, required=True)
    ap.add_argument("--repository-dir", type=pathlib.Path, required=True)
    args = ap.parse_args(args)
    thumbnailing(args.thumbnails_dir, args.repository_dir)


if __name__ == "__main__":
    main()
