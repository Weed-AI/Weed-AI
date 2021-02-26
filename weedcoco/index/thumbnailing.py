import argparse
import os
import json
import pathlib
from PIL import Image, ImageDraw
from weedcoco.utils import (
    check_if_approved_image_format,
    check_if_approved_image_extension,
    denormalise_weedcoco,
)


def _ensure_dir(path):
    if not os.path.isdir(os.path.dirname(str(path))):
        os.mkdir(os.path.dirname(str(path)))


def thumbnail_one(coco_image, image_path, thumbnails_dir, thumbnail_size):
    filename = os.path.basename(image_path)
    thumb_path = thumbnails_dir / filename[:2] / filename
    bbox_path = thumbnails_dir / ("bbox-" + filename[:2]) / filename

    image = Image.open(image_path)
    if not check_if_approved_image_format(image.format):
        # XXX: should this raise an error?
        return

    orig_width, orig_height = image.size
    image.thumbnail(thumbnail_size)
    thumb_width, thumb_height = image.size
    _ensure_dir(thumb_path)
    image.save(thumb_path)

    for annotation in coco_image["annotations"]:
        if "bbox" not in annotation:
            continue
        bx, by, bw, bh = annotation["bbox"]
        bx = bx * orig_width / thumb_width
        bw = bw * orig_width / thumb_width
        by = by * orig_height / thumb_height
        bh = bh * orig_height / thumb_height
        if annotation["category"]["name"].startswith("weed"):
            color = "#dc3545"
        elif annotation["category"]["name"].startswith("crop"):
            color = "#28a745"
        else:
            color = "#cccccc"

        draw = ImageDraw.Draw(image)
        draw.rectangle([bx, by, bx + bw, by + bh], outline=color)

    _ensure_dir(bbox_path)
    image.save(bbox_path)


def thumbnailing(
    thumbnails_dir, repository_dir, weedcoco_path, THUMBNAIL_SIZE=(300, 300)
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
                thumbnail_size=THUMBNAIL_SIZE,
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
