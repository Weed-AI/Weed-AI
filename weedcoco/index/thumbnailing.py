import argparse
import os
import pathlib
from PIL import Image


def thumbnailing(thumbnails_dir, repository_dir, THUMBNAIL_SIZE=(300, 300)):
    for dirpath, dirnames, filenames in os.walk(repository_dir):
        for filename in filenames:
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff")):
                image = Image.open(f"{dirpath}/{filename}")
                image.thumbnail(THUMBNAIL_SIZE)
                if filename[:2] not in os.listdir(thumbnails_dir):
                    os.mkdir(thumbnails_dir / filename[:2])
                image.save(thumbnails_dir / filename[:2] / filename)


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--thumbnails-dir", type=pathlib.Path, required=True)
    ap.add_argument("--repository-dir", type=pathlib.Path, required=True)
    args = ap.parse_args(args)
    thumbnailing(args.thumbnails_dir, args.repository_dir)


if __name__ == "__main__":
    main()
