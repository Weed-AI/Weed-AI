# About WeedCOCO

WeedCOCO is our format for representing weed identification annotations.

## Features

WeedCOCO extends upon the JSON-based [MS COCO (Microsoft Common Objects in
Context) image annotation format](https://cocodataset.org/#format-data) in
a few ways to support the agricultural and weed identification context.

As with MS COCO, the WeedCOCO format supports classification, bounding box and
segmentation labels, which together with a category naming sheme, are used to
indicate the presence of a specific or unknown species of weed, or presence
of the crop.

### Agricultural and Photographic Context

To apply machine learning into specific contexts, you need to train and
evaluate machine learning systems on controlled and focussed datasets.

WeedCOCO allows us to group annotated images by how they were captured: of what
crop in what stage of growth, with what camera setup, and in what conditions.
This additional annotation is known as "AgContext".

The *AgContext* component includes:

* Crop type
* Crop growth stage (text and BBCH)
* Soil colour
* Surface coverage
* Weather description
* Location
* Camera metadata (camera model, collection height, angle, lens, focal length, field of view)
* Lighting

You can use our [AgContext editor](/editor) to record the context of your
images.

### Category Names for Weed ID

Classification, bounding box and segmentation annotations may indicate:
* the presence of a known species of weed
* the presence of an unspecified type of weed
* the presence of crop

Category names should take the form `crop: <species name>` or `weed: <species
name>` where _species name_ is the scientific name of the crop or weed species.
If a weed is identified, but its species is not labelled, the appropriate
category name is `weed: UNSPECIFIED`. If annotations are used to mark non-weed,
non-crop spaces in the image, the appropriate category name is `none`.

### Richer Metadata

[Schema.org/dataset](https://schema.org/dataset)-compatible metadata is
required in the `'metadata'` key of the `'info'` blob.

Reporting these details will help ensure consistency in published
datasets for ease of comparison and use in further research and development.

## Importing Annotations and Validating WeedCOCO

We provide tools which may help convert your data to WeedCOCO. These can be
found in the `weedcoco` Python library which can be installed with:

```sh
$ pip install git+https://github.com/Sydney-Informatics-Hub/
```

Please see modules under the `weedcoco.importers` subpackage for conversion
into WeedCOCO format, and the `weedcoco.validation` module to validate your
JSON blob as compliant WeedCOCO.

## JSON Schema

The [JSON Schema](https://json-schema.org) specifying many aspects of valid
WeedCOCO data is found in YAML
[here](https://github.com/Sydney-Informatics-Hub/Weed-ID-Interchange/blob/master/weedcoco/schema).

## Contributing and Future Work

In the future we hope to:

* extend the format to distinguish between images intended for training data
  and those intended for test data.
* handle imagery with both visible-spectrum and near infrared (NIR) channels.

Contributions to our [open-source
repository](https://github.com/Sydney-Informatics-Hub/Weed-ID-Interchange) are
welcome to provide feedback on the WeedCOCO format, and to help resolve issues.
