import argparse
import os
import pathlib
from PIL import Image

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--thumbnails-dir", type=pathlib.Path, required=True)
ap.add_argument("--repository-dir", type=pathlib.Path, required=True)
args = ap.parse_args()

THUMBNAIL_SIZE = (300, 300)

for dirpath, dirnames, filenames in os.walk(args.repository_dir):
    for filename in filenames:
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff")):
            image = Image.open(f"{dirpath}/{filename}")
            image.thumbnail(THUMBNAIL_SIZE)
            if filename[:2] not in os.listdir(args.thumbnails_dir):
                os.mkdir(args.thumbnails_dir / filename[:2])
            image.save(args.thumbnails_dir / filename[:2] / filename)
