from collections import defaultdict
from pathlib import Path
from typing import Optional, Mapping
import argparse
import json
import yaml

from lxml import etree


def generate_coco_annotations(
    voc_objects: list, image_id: int, start_id: int, category_mapping: Mapping[str, int]
):
    for annotation_id, voc_object in enumerate(voc_objects, start_id):
        # TODO: handle segmented
        annotation = {
            "id": annotation_id,
            "image_id": image_id,
            "category_id": category_mapping[voc_object.find("name").text],
            # TODO: handle truncated, difficult?
        }
        voc_bndbox = voc_object.find("bndbox")
        if voc_bndbox is not None:
            dims = {elem.tag: int(elem.text) for elem in voc_bndbox}
            annotation["bbox"] = [
                dims["xmin"],
                dims["ymin"],
                dims["xmax"] - dims["xmin"] + 1,
                dims["ymax"] - dims["ymin"] + 1,
            ]
        yield annotation


def voc_to_coco(
    xml_dir: Path, image_dir: Path, category_mapping: Optional[Mapping[str, int]] = None
):
    """Convert VOC to MS COCO images and annotations

    Parameters
    ----------
    xml_dir : pathlib.Path
    image_dir : pathlib.Path
    category_mapping : Mapping
        By default, VOC's <name> will be used as the name of COCO categories,
        which will be numbered ordinally starting from 0.

    Returns
    -------
    dict
        Keys present should be 'images', 'annotations', and
        'categories' if category_mapping was not provided.
        Other COCO components should be added as a post-process.
    """
    use_default_category_mapping = True
    if use_default_category_mapping:
        category_mapping = defaultdict(None)
        # ordinal numbering
        category_mapping.default_factory = category_mapping.__len__

    images = []
    annotations = []
    for image_id, xml_path in enumerate(xml_dir.glob("*.xml")):
        voc_annotation = etree.parse(xml_path).getroot()
        assert voc_annotation.tag == "annotation"

        coco_image = {
            "id": image_id,
            # TODO: handle folder
            "file_name": voc_annotation.find("filename").text,
            "width": int(voc_annotation.find("size/width").text),
            "height": int(voc_annotation.find("size/height").text),
            # TODO: handle absent size
            # TODO: handle depth?
            # TODO: handle folder and path??
        }
        images.append(coco_image)

        annotations.extend(
            generate_coco_annotations(
                voc_annotation.findall("object"),
                image_id=image_id,
                base_annotation_id=len(annotations),
                category_mapping=category_mapping,
            )
        )

    if use_default_category_mapping:
        # TODO: define role somehow??
        categories = [
            {"id": idx, "name": name} for name, idx in category_mapping.items()
        ]

    return {"images": coco_image, "annotations": annotations, "categories": categories}


def _load_json_or_yaml(path):
    if path.endswith(".yaml"):
        obj = yaml.safe_load(path)
    else:
        obj = json.load(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--voc-dir", required=True, default=".", type=Path)
    ap.add_argument("--image-dir", required=True, type=Path)
    ap.add_argument("--agcontext-path", type=Path)
    ap.add_argument("--collection-path", type=Path)
    ap.add_argument("-o", "--out-path", default="coco_from_voc.json", type=Path)
    args = ap.parse_args()

    coco = voc_to_coco(args.voc_dir, args.image_dir)
    if args.agcontext_path:
        agcontext = _load_json_or_yaml(args.agcontext_path)
        if "id" not in agcontext:
            agcontext["id"] = 0
        coco["agcontexts"] = [agcontext]
        for image in coco["images"]:
            image["agcontext_id"] = agcontext["id"]

    if args.collection_path:
        collection = _load_json_or_yaml(args.collection_path)
        if "id" not in collection:
            collection["id"] = 0
        coco["collections"] = [collection]
        coco["collection_memberships"] = [
            {"annotation_id": annotation["id"], "collection_id": collection["id"]}
            for annotation in coco["annotations"]
        ]

    # TODO: validate

    with args.out_path.open("w") as out:
        json.dump(coco, out, indent=4)


if __name__ == "__main__":
    main()
