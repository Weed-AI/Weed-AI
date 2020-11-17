from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import random
import os
import cv2
from tensorflow.keras.preprocessing.image import ImageDataGenerator

### For visualizing the outputs ###
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
%matplotlib inline

### weedcoco utilities ###
from weedcoco.validation import validate
from weedcoco.utils import load_json_or_yaml
from weedcoco.utils import add_agcontext_from_file
from weedcoco.utils import add_collection_from_file

def create_sub_masks():


def create_sub_mask_anns(sub_mask, image_id, category_id, annotation_id, is_crowd):



    annotation = {
        'segmentation': segmentations,
        'iscrowd': is_crowd,
        'image_id': image_id,
        'category_id': category_id,
        'id': annotation_id,
        'bbox': bbox,
        'area': area
    }

    return annotation

def generate_mask_annotations():
    
    for annotation_id, voc_object in enumerate(voc_objects, start_id):
        # TODO: do we need to handle "segmented"?
        annotation = {
            "id": annotation_id,
            "image_id": image_id,
            "category_id": category_mapping[voc_object.find("name").text],
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