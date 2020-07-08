# Spec Overview

## Summary

To support an open weed image recognition database, we have worked on adapting existing image annotation standards to meet the unique needs of researchers and end users. There are multiple different competing standards for computer vision image annotations, however Microsoft's Common Objects in Context (COCO) standard has become increasingly dominant in the computer vision space. Our standard is an evolution or extension of COCO with ammendements to support our intended uses. While most computer vision annotation styles - including COCO - are designed primarily to support individual computer vision tasks or experiments, our annotation style is designed to also support many potential users uploading datasets, while also providing support for users searching, filtering, and downloading images and annotations from multiple different datasets. 

## Key features of the COCO format

COCO annotations are stored in single JSON files that contain annotations for each image in a dataset. This differs from other format like Pascal VOC, where annotations are stored in individual files for each image. The COCO format stores information in a way that is similar to a relational database. To explain what this means in practice, here is an example. Each annotation contains a value which indicates the category of the object in the annotation. Elsewhere in the document, there is a list of categories. This method storing data helps to limit duplication of information. 

The structure of COCO annotations is designed to support computer vision research primarily. Each COCO annotation file contains a list of all images in the dataset, with information about image size and image license stored at the image level. The actual annotations are stored as another list, with information specific to the type of annotation (classification, segmentation, etc.). Next, there is a list of categories that describe the annotations. Finally, there is an "info" section which provides some basic dataset wide information, and a "licenses" section with a list of all the licenses used by the images in the dataset.

## Adapting COCO to our needs

### Expanding the "categories" object

Genrally, COCO annotation categories only contain the name and id of each category. In the agricultural context, we are aware that different plants may play different roles in different scenarios (i.e. a plant may be a crop in one dataset and a weed in another). To capture this information, we have added in a "role" for each category.

```
    "categories": [

        {
            "name": "lantana",
            "id": 1,
            "role": "weed"
        },
        {
            "name": "triticum aestivum",
            "id": 2,
            "role": "crop"
        }
  ]
```

We are still determining the amount of information to include in categories: it may be good to include reference to information like Bayer codes, common names, or other information that is typically used with biological standards such as GBIF.

### The "collections" object

One of the key features we want to support is the ability for users to contribute their own images while also being able to assemble datasets from multiple different datasets that have previously been uploaded. To support this functionality, we have added another object which lists all of the important information about each specific collection of images. Each annotation is tied to a specific collection, and when a dataset is assembled by merging images/annotations from multiple different datasets, there will then be a seperate "collection" object for each of the different datasets. 

```
"collections": [
  {"id": 0,
   "title": "myweeds",
   "identifier": "doi:0000000/000000000000",
   "annotation_count": 158,
   "image_count": 104}
],
"collection_memberships": [
  {"annotation_id": 0,
   "collection_id": 0,
   "subset": "train"},
  {"annotation_id": 1,
   "collection_id": 0,
   "subset": "test"}
]
```

### The "agcontexts" object

The other key feature our data format must support is the ability to store and refer to information that is essential in the agricultural context. To do this we have created an object with the agricultural context. Each annotation then contains a key linking it to its specific agricultural context object.

```
    "agcontexts": [
        "agcontext": {
            "agcontext_id": "deepweeds",
            "crop_type": "pastoral_grassland",
            "upload_time": "2020-07-08 10:43:08",
            "camera_type": "weedlogger",
            "camera_angle": "90",
            "camera_fov": "85",
            "emr_channels": "na",
            "url": "https://github.com/AlexOlsen/DeepWeeds"}
    ]
```
