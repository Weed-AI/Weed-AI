from pathlib import Path
from typing import Mapping
import argparse
import json
import csv
from weedcoco.validation import validate
from weedcoco.utils import add_agcontext_from_file
from weedcoco.utils import add_metadata_from_file


CSV_COLS = ("filename", "category", "Negative")


def csv_to_coco(csv_path: Path, csv_mapping: Mapping[str, str]):
    images = []
    annotations = []
    categories = []

    with csv_path.open("r", newline="") as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        csv_dict = [
            row
            for row in csv.DictReader(csvfile, dialect=dialect, skipinitialspace=True)
        ]

    if len(csv_dict) == 0:
        raise ValueError("Empty csv file")

    for key in CSV_COLS:
        if key not in csv_mapping:
            raise ValueError(f"{key} is missing from the column mapping.")
        if csv_mapping[key] not in csv_dict[0] and key != "Negative":
            raise ValueError(f"{csv_mapping[key]} is missing from the csv file")

    images_dict = {}
    categories_dict = {}
    for row in csv_dict:
        temp_filename, temp_category = (
            row[csv_mapping["filename"]],
            row[csv_mapping["category"]],
        )
        if temp_category == csv_mapping["Negative"]:
            continue
        if temp_filename not in images_dict:
            image_id = len(images_dict)
            images_dict[temp_filename] = image_id
            images.append({"id": image_id, "file_name": temp_filename})
        if temp_category not in categories_dict:
            category_id = len(categories_dict)
            categories_dict[temp_category] = category_id
            categories.append({"id": category_id, "name": temp_category})
        annotations.append(
            {
                "image_id": images_dict[temp_filename],
                "category_id": categories_dict[temp_category],
            }
        )
    out = {
        "images": images,
        "annotations": annotations,
        "categories": categories,
        "info": {},
    }
    return out


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv-path", required=True, default=".", type=Path)
    ap.add_argument("--csv-mapping-path", required=True, default=".", type=Path)
    ap.add_argument("--agcontext-path", type=Path)
    ap.add_argument("--metadata-path", type=Path)
    ap.add_argument("--validate", action="store_true", default=False)
    ap.add_argument("-o", "--out-path", default="coco_from_csv.json", type=Path)
    args = ap.parse_args(args)

    with open(args.csv_mapping_path) as jsonfile:
        csv_mapping = json.load(jsonfile)
        coco = csv_to_coco(args.csv_path, csv_mapping)

    if args.agcontext_path:
        add_agcontext_from_file(coco, args.agcontext_path)
    if args.metadata_path:
        add_metadata_from_file(coco, args.metadata_path)

    if args.validate:
        validate(coco)

    with args.out_path.open("w") as out:
        json.dump(coco, out, indent=4)


if __name__ == "__main__":
    main()
