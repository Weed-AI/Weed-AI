@echo off
REM Set the directory here, it must have an folder name img and a folder name voc.
REM The folder must also contain the category-name-map.yaml file
set directory=path/to/your/directory/here
set cocoName=your-coco-name
REM set this as the path to your downloaded weedcoco directory
cd path/to/root/directory/of/weedai

REM uncomment either labelbox.py or voc.py depending on the one you want to use.

REM python voc.py^
REM --voc-dir path\to\upload-folder\voc^
REM --image-dir path\to\upload-folder\img^
REM --category-name-map path\to\upload-folder\category-name-map.yaml^
REM --agcontext-path path\to\upload-folder\agcontext.json^
REM -o path\to\upload-folder\cocoName-coco.json^
REM --metadata-path path\to\upload-folder\metadata.json^
REM --validate

python weedcoco/importers/labelbox.py^
 --labelbox-json %directory%\labelbox_output.json^
 --save-dir %directory%^
 --voc-to-coco^
 --keep-original-ID^
 --category-name-map %directory%\category-name-map.yaml^
 --agcontext-path %directory%\agcontext.json^
 -o %directory%\cocoName-coco.json^
 --metadata-path %directory%\metadata.json^
 --validate
 REM --start-index 1500
