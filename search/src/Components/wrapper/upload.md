## Annotation Formats

Annotations can currently be uploaded in the following formats, for which we note the supported annotation layers:

| Format | Classification | Bounding Boxes | Segmentation |
|:-------|:--------------:|:--------------:|:--------------:|
| [WeedCOCO](./weedcoco) | ✔️ | ✔️ | ✔️ |
| [MS COCO](https://cocodataset.org/#format-data) | ✔️ | ✔️ | ✔️ |
| Pascal VOC XML | | ✔️ | |
| Color-coded segmentation masks | | | ✔️ |

We natively support WeedCOCO format which extends on MS COCO to specify a weed
ID-oriented category naming scheme, to include agricultural context and
[schema.org/Dataset](https://schema.org/Dataset)-compatible metadata.
Uploads in other formats be converted to WeedCOCO format, with
forms to enter agricultural context and metadata, as well as to
map category names to our standardised nomenclature.

We require that contributors license their images and annotations under the
liberal [CC-BY 4.0 licence](https://creativecommons.org/licenses/by/4.0/)
(Creative Commons Attribution Required). Uploaders must have the rights to the
content that they upload, and must agree to release their content (images and
annotations) under the terms of that licence.

In brief (and not a substitute for the License), the CC BY 4.0 License enables
users to freely share and adapt the material for any purpose, even
commercially, given appropriate attribution and that there are no additional
restrictions made.


## Data Quality Requirements

Submitted datasets that contain any of the following will be rejected by
dataset reviewers:

* Irrelevant images (such as non-weed or crop imagery)
*  Poor image quality (over/under exposed, blurry images)
* Unlabelled or poorly labelled data
* Images with personally identifiable content (such as faces and vehicle details)
* Images with explicit content

Currently only new images to the repository will be accepted.

## Upload Process

The uploading process is a five-step process:

1. Select the data annotation format above.
2. Upload the annotation file. Please check that your images and annotations.
3. If not WeedCOCO, confirm a mapping from the entered category labels to role (weed or crop) and species.
4. If not WeedCOCO, upload the AgContext file or generate a new one by completing the online form.
5. Enter publication-level metadata about the dataset and how to attribute it.
6. Finally, upload the relevant images for the dataset

A Weed-AI administrator will review your submission. If the dataset is accepted
you will be notified and can continue uploading new datasets. The new dataset
will appear on the datasets page for other users to peruse.

Only one dataset per uploader can be in submission and review at any time.

## Prepare for your upload

Some tips to prepare your dataset:

1. [Construct and save an AgContext](/editor) (download it as JSON).
2. Get a DOI and [construct and save metadata](/meta-editor).
3. Get the annotations into MS COCO format. You might want to use the `weedcoco.importers` package of the [`weedcoco` Python library](https://github.com/Sydney-Informatics-Hub/Weed-ID-Interchange), or using a third party tool like [Roboflow](https://roboflow.com).
