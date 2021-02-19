@echo off
REM Set the directory here, it must have an folder name img and a folder name voc.
REM The folder must also contain the category-name-map.yaml file
set directory=Z:\weedAI_uploads\20190728
set cocoName=20190728v8

REM set this as the path to your downloaded weedcoco directory
cd C:\Users\gcol4791\PycharmProjects\Weed-ID-Interchange REM INSERT YOUR PATH TO VOC_CONVERT.PY HERE

python voc_to_coco.py^
 --voc-dir %directory%\voc^
 --image-dir %directory%\img^
 --category-name-map %directory%\category-name-map.yaml^
 --agcontext-path Z:\weedAI_uploads\20190728\agcontext.json^
 -o %directory%\%cocoName%-coco.json^
 --metadata-path %directory%\metadata1.json^
 --validate
