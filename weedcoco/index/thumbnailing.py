import argparse
import os
import json
import pathlib
from PIL import Image
from weedcoco.utils import (
    check_if_approved_image_format,
    check_if_approved_image_extension,
    denormalise_weedcoco,
)


THUMBNAIL_SIZES = {
    "": (300, 300),
    "lg-": (1000, 1000),
}


def _ensure_dir(path):
    if not os.path.isdir(os.path.dirname(str(path))):
        os.mkdir(os.path.dirname(str(path)))


def thumbnail_one(coco_image, image_path, thumbnails_dir, thumbnail_sizes):
    filename = os.path.basename(image_path)

    image = Image.open(image_path)
    if not check_if_approved_image_format(image.format):
        # XXX: should this raise an error?
        return

    for dir_prefix, thumbnail_size in thumbnail_sizes.items():
        thumb_path = thumbnails_dir / (dir_prefix + filename[:2]) / filename
        orig_width, orig_height = image.size
        thumb = image.copy()
        thumb.thumbnail(thumbnail_size)
        _ensure_dir(thumb_path)
        thumb.save(thumb_path)


def thumbnailing(
    thumbnails_dir, repository_dir, weedcoco_path, thumbnail_sizes=THUMBNAIL_SIZES
):
    with open(weedcoco_path) as f:
        coco = json.load(f)
    denormalise_weedcoco(coco)
    coco_by_filename = {
        os.path.basename(image["file_name"]): image for image in coco["images"]
    }

    for dirpath, dirnames, filenames in os.walk(repository_dir):
        for filename in filenames:
            if not check_if_approved_image_extension(filename):
                # XXX: should this raise an error?
                continue
            thumbnail_one(
                coco_by_filename[filename],
                f"{dirpath}/{filename}",
                thumbnails_dir,
                thumbnail_sizes=thumbnail_sizes,
            )


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--thumbnails-dir", type=pathlib.Path, required=True)
    ap.add_argument("--repository-dir", type=pathlib.Path, required=True)
    ap.add_argument("--weedcoco-path", type=pathlib.Path, required=True)
    args = ap.parse_args(args)
    thumbnailing(args.thumbnails_dir, args.repository_dir, args.weedcoco_path)


if __name__ == "__main__":
    main()
