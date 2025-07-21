from pathlib import Path
import yaml
import json
from weedcoco.utils import get_image_dimensions, add_agcontext_from_file, add_metadata_from_file, check_if_approved_image_extension
from weedcoco.validation import validate
import argparse


def yolo_to_coco(yolo_dir: Path, image_dir: Path):
    """
    Convert YOLO to MS COCO images and annotations.
    Assumes image_dir is populated with the corresponding images.
    """
    images = []
    annotations = []
    categories = []

    try:
        yaml_path = next(yolo_dir.glob("*.yaml"))
        with open(yaml_path) as f:
            yolo_yaml = yaml.safe_load(f)

        for i, name in enumerate(yolo_yaml['names']):
            categories.append({"id": i, "name": name})

    except StopIteration:
        raise FileNotFoundError("Could not find a .yaml file in the yolo directory")

    annotation_id_counter = 0
    image_id_counter = 0

    image_files = {p.stem: p for p in image_dir.glob("*") if check_if_approved_image_extension(p.name)}

    for txt_path in sorted(yolo_dir.glob("*.txt")):
        if txt_path.stem not in image_files:
            print(f"Warning: Skipping annotation '{txt_path.name}' because no matching image was found.")
            continue

        image_path = image_files[txt_path.stem]
        image_name = image_path.name

        # Get actual image dimensions
        dims = get_image_dimensions(image_path)
        if not dims:
            print(f"Warning: Could not read dimensions for image '{image_name}'. Skipping.")
            continue
        width, height = dims['width'], dims['height']

        images.append({
            "id": image_id_counter,
            "file_name": image_name,
            "width": width,
            "height": height,
        })

        with open(txt_path) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 5:
                    continue

                class_id, x_center, y_center, bbox_width, bbox_height = map(float, parts)

                x_min = (x_center - bbox_width / 2) * width
                y_min = (y_center - bbox_height / 2) * height
                w = bbox_width * width
                h = bbox_height * height

                annotations.append({
                    "id": annotation_id_counter,
                    "image_id": image_id_counter,
                    "category_id": int(class_id),
                    "bbox": [x_min, y_min, w, h],
                    "area": w * h,
                    "iscrowd": 0,
                })
                annotation_id_counter += 1

        image_id_counter += 1

    return {
        "images": images,
        "annotations": annotations,
        "categories": categories,
        "info": {}
    }


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yolo-dir", required=True, type=Path)
    ap.add_argument("--image-dir", required=True, type=Path)
    ap.add_argument("--agcontext-path", type=Path)
    ap.add_argument("--metadata-path", type=Path)
    ap.add_argument("--validate", action="store_true", default=False)
    ap.add_argument("-o", "--out-path", default="coco_from_yolo.json", type=Path)
    args = ap.parse_args(args)

    coco = yolo_to_coco(args.yolo_dir, args.image_dir)

    if not coco["images"]:
        ap.error(f"Found no .txt files in {args.yolo_dir}")

    if args.agcontext_path:
        add_agcontext_from_file(coco, args.agcontext_path)
    if args.metadata_path:
        add_metadata_from_file(coco, args.metadata_path)
    if args.validate:
        validate(coco, schema="compatible-coco")

    with args.out_path.open("w") as out:
        json.dump(coco, out, indent=4)


if __name__ == "__main__":
    main()