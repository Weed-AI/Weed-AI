# Welcome to Weed-AI.

### *Supporting the AI revolution in weed control*

Weeds, by definition, are plants in the wrong place but Weed-AI is helping put weed image data in the right place. Weed-AI is an open source, searchable, weeds image data platform designed to facilitate the research and development of machine learning algorithms for weed recognition in cropping systems.

# The need for AI in weed control

The default method of weed control in large-scale agriculture is field-wide treatments. Site-specific weed control (SSWC) is a more fine-grained approach where weed control treatments are applied only to targeted weeds. Under this approach, off-target land and crop are not exposed to the weed control method. Compared to field-wide herbicide treatments, the volume of herbicide applied to the land under SSWC is dramatically reduced. By performing targeted weed control, in-crop, SSWC also enables the use of novel, non-selective weed control technologies (such as lasers, microwaves and electrocution).

The success of SSWC depends on accurate detection and localisation of weeds, the combination termed weed recognition. While many powerful algorithms have been published for detection and recognition tasks, they have been trained on urban data. Unlike objects typical of urban scenes, crop and weeds display highly variable morphologies as they grow. There can be strong similarities between crop and weeds, particularly for closely related species. Adapting the state-of-the-art classification, detection and segmentation algorithms requires the availability of large quantities adequate training data. A major bottleneck in the development of effective weed recognition is annotating imagery, a typically slow and labour-intensive process. Weed-AI is addressing these challenges by enabling the easy access and contribution of annotated weed image data with standardised metadata on an open source platform with upload, search, dynamic filter and preview functions.

## How is Weed-AI different?

Currently publicly available weed datasets are fragmented and collected, stored and managed by multiple institutions. While the availability of this data is beneficial, this piecemeal approach lacks standards, structure, user-friendly search and the convenience of storing datasets together in one place. For example, a [review](https://www.sciencedirect.com/science/article/pii/S0168169920312709) of weed-specific datasets by Lu and Young 2020 found 15 were available at the time of writing each with varying degrees of metadata and all in different locations for download.

Weed-AI supports the contribution of users' own annotated weeds image data, browsing of existing data on the platform and download of whole datasets in a simple click.

# Navigating Weed-AI

### Explore

The [Explore](/explore) tab lets you filter and search all currently available datasets to find the image data that suit your purposes. Selecting an image will take you to the dataset summary page, providing detail on the dataset wide metadata including information such as camera specifications, crop stage and background conditions.

### Datasets

The datasets are listed on the [Datasets](/datasets) page. Select any dataset to read dataset wide metadata, to view image samples and to download the complete dataset.

### Upload

Contributing your own datasets to Weed-AI is streamlined on the [Upload](/upload) page. Create a Weed-AI account or log in with your Google details to begin the upload process. Upon completion of the upload steps described below, your dataset will be sent for review with the outcome provided on this page. Only one dataset per uploader can be in review at any time.

# Data types supported

To support the largest number of use cases, the unique demands of SSWC technology development and to ensure future utility of the system, we have developed a standard for storing annotated weeds image data.

Our standard, **WeedCOCO**, is an extension on Microsoft's Common Objects in Context format (MS COCO). WeedCOCO incorporates additional whole-dataset contextual information that provides descriptions of the agricultural context as well as details of how the images were capture. This *AgContext* component includes:

* Crop type
* Crop growth stage (text and BBCH)
* Soil colour
* Surface coverage
* Weather description
* Location
* Camera metadata (camera model, collection height, angle, lens, focal length, field of view)
* Lighting

As with MS COCO, the WeedCOCO format supports classification, bounding box and segmentation labels indicating the presence of a specific or unknown species of weed. Reporting these details will help ensure consistency in published datasets for ease of comparison and use in further research and development.

## Uploading Data

The uploading process is a five-step process:

1. Navigate to the upload tab, and select the data annotation format.

2. Upload the annotation file. Only COCO or WeedCOCO are supported currently.

3. If not WeedCOCO, upload the AgContext file or generate a new one by completing the online form.

4. Include any additional dataset metadata.

5. Finally, upload the relevant images for the dataset

Upon submission of your dataset, a request for review will be sent to a Weed-AI administrator. If the dataset is accepted you will be notified and can continue uploading new datasets. The new dataset will appear on the datasets page for other users to peruse.

## Data quality requirements

Submitted datasets that contain any of the following will be rejected by dataset reviewers:

* Irrelevant images (such as non-weed or crop imagery)
*  Poor image quality (over/under exposed, blurry images)
* Unlabelled or poorly labelled data
* Images with personally identifiable content (such as faces and vehicle details)
* Images with explicit content


## About WeedCOCO

WeedCOCO is our format for representing weed identification annotations.

### Features

WeedCOCO extends upon the JSON-based [MS COCO image annotation format](https://cocodataset.org/#format-data) in the following ways:

* **Category Names**: Annotations should target the presence of crop or weed. Category names should take the form `crop: <species name>` or `weed: <species name>` where _species name_ is the scientific name of the crop or weed species. If a weed is identified, but its species is not labelled, the appropriate category name is `weed: unspecified`. If annotations are used to mark non-weed, non-crop spaces in the image, the appropriate category name is `none`.
* **Agricultural and Photographic Context**: To support the construction of controlled and site-appropriate machine-learning based weed identification, WeedCOCO datasets group their images by how they were captured: of what crop in what stage of growth, with what camera setup, and in what conditions. This additional annotation is known as "AgContext". You can use our [AgContext editor](/editor) to record the context for your image capture session.
* **Richer Metadata**: [Schema.org/dataset](https://schema.org/dataset)-compatible metadata is required in the `'metadata'` key of the `'info'` blob.

In the future we hope to:

* extend the format to distinguish between images intended for training data and those intended for test data.
* handle imagery with both visible-spectrum and near infrared (NIR) channels.

## Importing Annotations and Validating WeedCOCO

We provide tools which may help convert your data to WeedCOCO. These can be found in the `weedcoco` Python library which can be installed with:

```sh
$ pip install git+https://github.com/Sydney-Informatics-Hub/
```
Please see modules under the `weedcoco.importers` subpackage for conversion into WeedCOCO format, and the `weedcoco.validation` module to validate your JSON blob as compliant WeedCOCO.

## JSON Schema

The [JSON Schema](https://json-schema.org) specifying many aspects of valid WeedCOCO data is found in YAML [here](https://github.com/Sydney-Informatics-Hub/Weed-ID-Interchange/blob/master/weedcoco/schema).



# Data Licensing

All image data uploaded to Weed-AI is bound by the **CC BY 4.0 License**. Contributors must accept the terms of this license to upload image data. In brief (and not a substitute for the License), the CC BY 4.0 License enables users to freely share and adapt the material for any purpose, even commercially, given appropriate attribution and that there are no additional restrictions made. The CC BY 4.0 License is available [here](https://creativecommons.org/licenses/by/4.0/).

# Acknowledgements
The development of Weed-AI has been funded by the [Grains Research and Development Corporation (GRDC)](https://grdc.org.au) PROC-9175960 grant. The platform was developed by the [Sydney Informatics Hub](https://www.sydney.edu.au/research/facilities/sydney-informatics-hub.html), a core research facility of the University of Sydney, as part of a research collaboration with the [Australian Centre for Field Robotics](https://www.sydney.edu.au/engineering/our-research/robotics-and-intelligent-systems/australian-centre-for-field-robotics.html) and the [Precision Weed Control Group](https://www.sydney.edu.au/science/our-research/research-areas/life-and-environmental-sciences/precision-weed-control-group.html) at the University of Sydney.

The software is open source and open to contribution on [GitHub](https://github.com/Sydney-Informatics-Hub/Weed-ID-Interchange). If you have any issues, suggestions or would like to contribute to the project please do so through weed-ai@sydney.edu.au or GitHub.

[![The University of Sydney logo](/usyd-logo.png "The University of Sydney")](https://sydney.edu.au)

# Citation Guidelines

## General

If you found Weed-AI useful in your research or project, please cite the database as:

CITATION TBA by mid 2021

## Specific Datasets

Each set of imagery used within the database should also be cited with the correct database Digital Object Identifier (DOI) and relevant papers.

# Privacy

The collection of information is bound by our Privacy Policy.
