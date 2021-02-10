# About WeedCOCO

WeedCOCO is our format for representing weed identification annotations.

## Features

WeedCOCO extends upon the JSON-based [MS COCO image annotation format](https://cocodataset.org/#format-data) in the following ways:

* **Category Names**: Annotations should target the presence of crop or weed. Category names should take the form `crop: <species name>` or `weed: <species name>` where _species name_ is the scientific name of the crop or weed species. If a weed is identified, but its species is not labelled, the appropriate category name is `weed: unspecified`. If annotations are used to mark non-weed, non-crop spaces in the image, the appropriate category name is `none`.
* **Agricultural and Photographic Context**: To support the construction of controlled and site-appropriate machine-learning based weed identification, WeedCOCO datasets group their images by how they were captured: of what crop in what stage of growth, with what camera setup, and in what conditions. This additional annotation is known as "AgContext". You can use our [AgContext editor](/editor) to record the context for your image capture session.
* **Richer Metadata**: [Schema.org/dataset](https://schema.org/dataset)-compatible metadata is required in the `'metadata'` key of the `'info'` blob.

In the future we hope to:

* extend the format to distinguish between images intended for training data and those intended for test data.
* handle imagery with both visible-spectrum and near infrared (NIR) channels.

## Contributing

Contributions to our [open-source repository](https://github.com/Sydney-Informatics-Hub/Weed-ID-Interchange) are welcome to provide feedback on the WeedCOCO format, and to help resolve issues.

## Importing Annotations and Validating WeedCOCO

We provide tools which may help convert your data to WeedCOCO. These can be found in the `weedcoco` Python library which can be installed with:

```sh
$ pip install git+https://github.com/Sydney-Informatics-Hub/
```

Please see modules under the `weedcoco.importers` subpackage for conversion into WeedCOCO format, and the `weedcoco.validation` module to validate your JSON blob as compliant WeedCOCO.

## JSON Schema

The [JSON Schema](https://json-schema.org) specifying many aspects of valid WeedCOCO data is found in YAML [here](https://github.com/Sydney-Informatics-Hub/Weed-ID-Interchange/blob/master/weedcoco/schema).
```
