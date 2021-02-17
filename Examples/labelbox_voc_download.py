from weedcoco.importers.voc import voc_to_coco
from weedcoco.validation import validate
from pascal_voc_writer import Writer
from pathlib import Path
from tqdm.auto import trange
import argparse
import requests
import shutil
import time
import json
import cv2
import os

def download_png(url, name, saveDir):
    '''
    Downloads an image from a URL and saves it with the name and save directory
    :param url: image url
    :param name: name of the image
    :param saveDir: save directory
    :return:
    '''
    image = requests.get(url, stream=True)
    if image.status_code == 200:
        image.raw.decode_content = True
        imagePath = os.path.join(saveDir, name)

        with open(imagePath, "wb") as handler:
            shutil.copyfileobj(image.raw, handler)

        image = cv2.imread(imagePath)
        cv2.imwrite(imagePath, image)
        print("[INFO] {} downloaded successfully".format(imagePath))

        return image, imagePath

    else:
        print("[ERROR] {} not downloaded...".format(name))
        return None

def check_labelbox_review_score(labelSet):
    '''
    Checks the review score from the labelbox json so only those datasets with positive reviews are downloaded
    :param labelSet: the labels for the image object
    :return: returns the review score
    '''
    try:
        reviews = labelSet['Reviews'][0]
        score = reviews['score']
    except IndexError:
        print("[INFO] {} skipped. NOT reviewed.".format(labelSet['External ID']))
        score = -1
    return score

def download_labelbox_images_voc(labelboxJSONPath, saveDir, keepExternalID=True, startIndex=0,
                                 saveImageDir=None, saveVOCDir=None):
    '''

    :param keepExternalID:
    :param startIndex:
    :return:
    '''
    imageLog = {}

    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    if saveImageDir is None:
        saveImageDir = os.path.join(saveDir, time.strftime("%Y%m%d") + "-img")
        if not os.path.exists(saveImageDir):
            os.mkdir(saveImageDir)

    if saveVOCDir is None:
        saveVOCDir = os.path.join(saveDir, time.strftime("%Y%m%d") + "-voc")
        if not os.path.exists(saveVOCDir):
            os.mkdir(saveVOCDir)

    with open(labelboxJSONPath, "r+") as f:
        labelboxJSON = json.load(f)
        print("[INFO] JSON {} loaded".format(labelboxJSONPath))

    # start downloading from a specific point
    for i in trange(startIndex, len(labelboxJSON), desc="Original Download"):
        labelSet = labelboxJSON[i]
        try:
            objectList = labelSet['Label']['objects']
        except KeyError:
            print('[ERROR] {} skipped - not labelled'.format(labelSet['External ID']))

        if check_labelbox_review_score(labelSet) == 1 and len(objectList) > 0:
            try:
                sequentialImageName = "image_" + str(i) + ".jpg"
                # remove any extra spaces in the name
                imageLog[sequentialImageName] = labelSet['External ID'].replace(" ", "")

                # keep the original image names on labelbox
                if keepExternalID:
                    imageName = labelSet['External ID'].replace(" ", "")
                    vocName = labelSet['External ID'].split('.')[0] + '.xml'
                else:
                    imageName = sequentialImageName
                    vocName = sequentialImageName.split('.')[0] + ".xml"

                # get the image URL and download the data
                origImgURL = labelSet['Labeled Data']
                image, imagePath = download_png(origImgURL, imageName, saveImageDir)

                # instantiate the VOC writer
                vocWriter = Writer(imagePath, height=image.shape[0], width=image.shape[1])

                # iterate over each object in the list
                for object in objectList:
                    className = object['title']
                    bbox = object['bbox']
                    startX = bbox['left']
                    startY = bbox['top']
                    endX = startX + bbox['width']
                    endY = startY + bbox['height']

                    vocWriter.addObject(className, startX, startY, endX, endY)
                vocPath = os.path.join(saveVOCDir, vocName)
                vocWriter.save(vocPath)

            except KeyError:
                print("[INFO] No objects found")
        else:
            print("[INFO] Image {} skipped".format(i))

    return Path(saveImageDir), Path(saveVOCDir)

def main():
    ap = argparse.ArgumentParser(description=__doc__)

    ap.add_argument("--labelbox-json", required=True, type=str, help='path to downloaded labelbox JSON file')
    ap.add_argument("--save-dir", required=True, type=str)
    ap.add_argument("--keep-original-ID", default=True, type=bool)
    ap.add_argument("--voc-to-coco", default=True, type=bool)
    ap.add_argument("--start-index", default=0, type=int)
    ap.add_argument("--save-image-dir", type=str, help='existing save directory for images')
    ap.add_argument("--save-voc-dir", type=str, help='existing save directory for VOC files')
    ap.add_argument("--validate", action="store_true", default=False)
    ap.add_argument("-o", "--out-path", default="coco_from_voc.json", type=Path)
    args = ap.parse_args()

    imageDir, vocDir = download_labelbox_images_voc(labelboxJSONPath=args.labelbox_json, saveDir=args.save_dir,
                                                    keepExternalID=args.keep_original_ID, startIndex=args.start_index,
                                                    saveImageDir=args.save_image_dir, saveVOCDir=args.save_voc_dir)

    if args.voc_to_coco:
        coco = voc_to_coco(vocDir, imageDir)

        if args.validate:
            validate(coco)

        with args.out_path.open("w") as out:
            json.dump(coco, out, indent=4)


if __name__ == "__main__":
    main()
