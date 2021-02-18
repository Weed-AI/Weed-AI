@echo off
REM Set the directory here, it must have an folder name img and a folder name voc.
REM The folder must also contain the category-name-map.yaml file
set directory=Z:\weedAI_uploads\20200701_cp_st2_19345082
set cocoName=20200701_cp_st2_19345082

REM set this as the path to your downloaded weedcoco directory
cd "C:\Users\gcol4791\PycharmProjects\Weed-ID-Interchange\Examples"

python voc_to_coco.py^
 --voc-dir %directory%\voc^
 --image-dir %directory%\img^
 --category-name-map %directory%\category-name-map.yaml^
 -o %directory%\%cocoName%-coco.json^
 --vis-an
 REM --validate
 REM --agcontext-path Z:\weedAI_uploads\20190728\agcontext.yaml^
