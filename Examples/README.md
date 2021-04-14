# Uploading your Own Data
The main feature of Weed-AI is the ability for users to contribute their own data to the platform. 
The following is a step-by-step guide on downloading data from a popular online annotation service Labelbox,
converting it to COCO, creating the *AgContext* and metatdata files and uploading it to Weed-AI.

Alternatively, if you are using one of the other labeling services below that produces VOC annotations
follow these instructions starting at Step XX. This will explain the conversion from VOC to COCO and
subsequent upload.

## Step 1: Downloading the LabelBox JSON
Once you have labelled your images to the standard required for the database in the Labelbox editor, download
the JSON and save it into your upload folder. Use the directory structure provided below:

```
upload folder
├── img
│   ├── all your images will end up here
│   └── weed1.png
├── voc
    ├── all you .xml files will end up here
    ├── weed1.xml
├── agcontext.json
├── metadata.json
├── category-name-map.yaml
└── labelbox_output.json

```
The `labelbox.py` converter will automatically create your img and voc directories in the structure above, so no
need to create those yourself. The agcontext.json and metadata.json files can be generated using the 
[agcontext](https://weed-ai.sydney.edu.au/editor)
and [metadata](https://weed-ai.sydney.edu.au/meta-editor) editors.

## Step 2: Download images, annotations and convert to COCO
Install the repository as per the [instructions](https://weed-ai.sydney.edu.au/weedcoco) to get access to the importers.
Once installed and working correctly, open a terminal/command line window (in Windows) and run:
```shell script
python labelbox.py^
 --labelbox-json path\to\upload-folder\labelbox_output.json^
 --voc-to-coco^
 --keep-original-ID^
 --voc-dir path\to\upload-folder\voc^
 --image-dir path\to\upload-folder\img^
 --category-name-map path\to\upload-folder\category-name-map.yaml^
 --agcontext-path path\to\upload-folder\agcontext.json^
 -o path\to\upload-folder\cocoName-coco.json^
 --metadata-path path\to\upload-folder\metadata.json^
 --validate
```
`labelbox.py` will convert the Labelbox output firstly to PASCAL VOC and then subsequently to weedCOCO based on the 
agcontext and metadata provided.

## Step 2a: Convert VOC annotations to COCO (without downloading from Labelbox)
Alternatively if you already have the VOC annotations handy, you can use the `voc.py` converter. In the command line enter:
```shell script
python voc.py^
 --voc-dir path\to\upload-folder\voc^
 --image-dir path\to\upload-folder\img^
 --category-name-map path\to\upload-folder\category-name-map.yaml^
 --agcontext-path path\to\upload-folder\agcontext.json^
 -o path\to\upload-folder\cocoName-coco.json^
 --metadata-path path\to\upload-folder\metadata.json^
 --validate
``` 

## Step 3: Upload!
That's it! You're ready to upload.

Great work, you have now contributed to the Weed-AI community and the development of opensource weed
recognition. The upload will be reviewed by the Weed-AI administrators and either accepted or rejected
based on data and annotation quality.