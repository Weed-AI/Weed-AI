from collections import defaultdict
from pathlib import Path
from typing import Optional, Mapping
import argparse
import json

# don't want to break everything if these modules are not installed just for visualising
try:
    from pycocotools.coco import COCO
    import matplotlib.pyplot as plt
    import numpy as np
    import time
    import cv2
    import os

    visualisation = True
except ModuleNotFoundError:
    visualisation = False

from lxml import etree

from weedcoco.validation import validate
from weedcoco.utils import load_json_or_yaml
from weedcoco.utils import add_agcontext_from_file
from weedcoco.utils import add_collection_from_file


def generate_coco_annotations(
    voc_objects: list, image_id: int, start_id: int, category_mapping: Mapping[str, int]
):
    for annotation_id, voc_object in enumerate(voc_objects, start_id):
        # TODO: do we need to handle "segmented"?
        annotation = {
            "id": annotation_id,
            "image_id": image_id,
            "category_id": category_mapping[voc_object.find("name").text],
            "segmentation": []
            # TODO: do we need to handle "truncated", "difficult"?
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
    use_default_category_mapping = category_mapping is None
    if use_default_category_mapping:
        category_mapping = defaultdict(None)
        # ordinal numbering
        category_mapping.default_factory = category_mapping.__len__

    images = []
    annotations = []
    for image_id, xml_path in enumerate(sorted(xml_dir.glob("[a-zA-Z0-9_]*.xml"))):
        voc_annotation = etree.parse(str(xml_path)).getroot()
        assert voc_annotation.tag == "annotation"

        coco_image = {
            "id": image_id,
            "file_name": voc_annotation.find("filename").text,
            "width": int(voc_annotation.find("size/width").text),
            "height": int(voc_annotation.find("size/height").text),
            # XXX: should we calculate height and width if absent?
            # TODO: handle folder and path??
        }
        images.append(coco_image)

        annotations.extend(
            generate_coco_annotations(
                voc_annotation.findall("object"),
                image_id=image_id,
                start_id=len(annotations),
                category_mapping=category_mapping,
            )
        )

    out = {"images": images, "annotations": annotations, "info": {}}
    if use_default_category_mapping:
        out["categories"] = [
            {"id": idx, "name": name} for name, idx in category_mapping.items()
        ]

    return out

def inspect_annotations(cocofile, saveImageDir, inspectNumber=5):
    '''
    Displays a random selection of images and annotations for a sanity check to make sure the conversion worked
    :param cocofile: path to the cocofile, not the file itself
    :param saveImageDir: directory of the images
    :param inspectNumber: number to inspect
    :return:
    '''
    # load the file using pycocotools
    annotations = COCO(annotation_file=cocofile)
    imgIDs = annotations.getImgIds()

    # iterate over random selection
    for i in range(inspectNumber):
        randID = imgIDs[np.random.randint(0, len(imgIDs))]
        annIDs = annotations.getAnnIds(imgIds=[randID])
        imageAnnotations = annotations.loadAnns(annIDs)
        imageInfo = annotations.loadImgs([randID])[0]
        imagePath = os.path.join(saveImageDir, imageInfo['file_name'])
        image = cv2.imread(imagePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        plt.figure()
        plt.axis('off')
        plt.imshow(image)

        # use the inbuilt pycocotools showAnns function to display the annotation
        annotations.showAnns(imageAnnotations, draw_bbox=True)
        plt.show()

def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--voc-dir", required=True, default=".", type=Path)
    ap.add_argument("--image-dir", required=True, type=Path)
    ap.add_argument(
        "--category-name-map",
        type=Path,
        help="JSON or YAML mapping of VOC names to WeedCOCO category names",
    )
    ap.add_argument("--agcontext-path", type=Path)
    ap.add_argument("--collection-path", type=Path)
    ap.add_argument("--vis-ann", action="store_true", default=False)
    ap.add_argument("--validate", action="store_true", default=False)
    ap.add_argument("-o", "--out-path", default="coco_from_voc.json", type=Path)
    args = ap.parse_args(args)

    if args.category_name_map:
        category_name_map = load_json_or_yaml(args.category_name_map)
        keys, values = zip(*category_name_map.items())
        categories = [{"id": i, "name": value} for i, value in enumerate(values)]
        category_mapping = {key: i for i, key in enumerate(keys)}
    else:
        categories = None
        category_mapping = None

    coco = voc_to_coco(args.voc_dir, args.image_dir, category_mapping=category_mapping)

    if not coco["images"]:
        ap.error(f"Found no .xml files in {args.voc_dir}")

    if categories is not None:
        coco["categories"] = categories
    if args.agcontext_path:
        add_agcontext_from_file(coco, args.agcontext_path)
    if args.collection_path:
        add_collection_from_file(coco, args.collection_path)

    if args.validate:
        validate(coco)

    with args.out_path.open("w") as out:
        json.dump(coco, out, indent=4)

    if args.vis_ann and visualisation:
        inspect_annotations(cocofile=args.out_path, saveImageDir=args.image_dir)


if __name__ == "__main__":
    main()
