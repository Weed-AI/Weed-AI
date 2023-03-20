MINIMAL_WEEDCOCO = {
    "images": [],
    "annotations": [],
    "categories": [],
    "agcontexts": [],
    "info": {
        "description": "Something",
        "metadata": {
            "name": "Something",
            "description": "Images of weeds",
            "creator": [{"@type": "Person", "name": "Someone"}],
            "datePublished": "XXXX-XX-XX",
            "license": "https://creativecommons.org/licenses/by/4.0/",
        },
    },
}

#Ambrosia, Euphorbia
DOUBTFUL_GENUS_WEEDCOCO = {
    "images": [
        {
            "id": 0,
            "folder": "C:\\Users\\gcol4791\\Downloads\\CottonWeedDet12\\weedImages",
            "file_name": "20210820_iPhoneSE_YL_1562.jpg",
            "width": 3024,
            "height": 4032,
            "depth": "3"
        },
        {
            "id": 1,
            "folder": "C:\\Users\\gcol4791\\Downloads\\CottonWeedDet12\\weedImages",
            "file_name": "20210912_iPhoneSE_YL_76.jpg",
            "width": 3024,
            "height": 4032,
            "depth": "3"
        },
    ],
    "annotations":[
        {
            "image_id": 0,
            "id": 0,
            "segmented": "0",
            "bbox": [
                2834.0,
                3097.0,
                190.0,
                477.0
            ],
            "area": 90630.0,
            "iscrowd": 0.0,
            "pose": "Unspecified",
            "truncated": "0",
            "category_id": 0,
            "difficult": "0"
        },
        {
            "image_id": 1,
            "id": 1,
            "segmented": "0",
            "bbox": [
                1201.0,
                316.0,
                538.0,
                671.0
            ],
            "area": 360998.0,
            "iscrowd": 0.0,
            "pose": "Unspecified",
            "truncated": "0",
            "category_id": 1,
            "difficult": "0"
        },
    ],
    "categories":[
        {
            "name": "weed: ambrosia",
            "common_name": "ragweed",
            "species": "ambrosia",
            "role": "weed",
            "id": 0,
        },
        {
            "name": "weed: euphorbia",
            "common_name": "spurge",
            "species": "euphorbia",
            "role": "weed",
            "id": 1,
        },
    ],
    "agcontexts":[
        {
          "id": 0,
          "crop_type": "",
          "bbch_growth_range": "",
          "soil_colour": "variable",
          "surface_cover": "cereal",
          "surface_coverage": "0-25",
          "location_lat": 33.453808,
          "location_long": -88.790587,
          "camera_make": "iPhoneSE, iPhone11Pro, NIKON D3300, Canon EOS4000D",
          "camera_lens": "Mixed",
          "camera_lens_focallength": 0,
          "camera_height": 400,
          "camera_angle": 90,
          "camera_fov": "variable",
          "ground_speed": 0,
          "lighting": "natural",
          "photography_description": "From the publication: The weed dataset, CottonWeedDet12 was collected using different hand-held smartphones and digital color cameras (with resolution of more than 10 megapixels). Images were collected under natural field light conditions and different weather conditions (e. g., sunny, cloudy, and overcast) at varying stages of weed growth and different field sites. Regular visits to cotton fields, after crop emergence until canopy closure, were conducted throughout June to September of 2021 for weed image collection. Images are largely centered on each plant.",
          "weather_description": "Collected under all conditions, sunny, cloudy and overcast"
        }
    ],
    "info": {
        "metadata": {
          "description": "The dataset CottonWeedDet12 consists of 5648 RGB images of 12-class weeds that are common in cotton fields in the southern U.S. states, with a total of 9370 bounding boxes. These images were acquired by either smartphones or hand-held digital cameras, under natural field light condition and throughout June to September of 2021. The images were manually labeled by qualified personnel for weed identification, and the labeling process was done using the VGG Image Annotator (version 2.10).\n\nThe dataset, at the time of publication, is the largest publicly available multi-class dataset dedicated to weed detection. It expects to facilitate communicate efforts to exploit state-of-the-art deep learning method to push weed recognition to the next level. With the WeedDet12 dataset, a performance benchmark of a suite of YOLO object detectors has been built for weed detection. Detailed documentation of the dataset, model benchmarking and performance results is given in an accompanying journal paper paper: Dang, F., Chen, D., Lu, Y., Li, Z., 2023. YOLOWeeds: A novel benchmark of YOLO object detectors for multi-class weed detection in cotton production systems. Computers and Electronics in Agriculture. https://doi.org/10.1016/j.compag.2023.107655 ",
          "license": "https://creativecommons.org/licenses/by/4.0/",
          "@type": "Dataset",
          "name": "CottonWeedDet12",
          "datePublished": "2023-01-13",
          "creator": [
            {
              "@type": "Person",
              "affiliation": {
                "@type": "Organization",
                "name": "Michigan State University"
              },
              "name": "Fengying Dang"
            },
            {
              "@type": "Person",
              "affiliation": {
                "@type": "Organization",
                "name": "Michigan State University"
              },
              "name": "Dong Chen"
            },
            {
              "@type": "Person",
              "affiliation": {
                "@type": "Organization",
                "name": "Michigan State University"
              },
              "name": "Yuzhen Lu"
            },
            {
              "@type": "Person",
              "affiliation": {
                "@type": "Organization",
                "name": "Mississippi State University"
              },
              "name": "Zhaojian Li"
            }
          ],
          "citation": "https://www.sciencedirect.com/science/article/abs/pii/S0168169923000431",
          "identifier": [
            "https://zenodo.org/record/7535814#.Y9u3ZnbMJaQ"
          ],
          "sameAs": [
            "https://github.com/DongChen06/DCW"
          ],
          "funder": [
            {
              "@type": "Organization",
              "name": "Cotton Incorporated"
            }
          ]
        },
    },
}

SMALL_WEEDCOCO = {
    "images": [
        {
            "id": 46,
            "file_name": "cwfid_images/046_image.png",
            "license": 0,
            "agcontext_id": 0,
            "width": 1296,
            "height": 966,
        },
        {
            "id": 1,
            "file_name": "cwfid_images/001_image.png",
            "license": 0,
            "agcontext_id": 0,
            "width": 1296,
            "height": 966,
        },
    ],
    "annotations": [
        {
            "id": 0,
            "image_id": 46,
            "category_id": 0,
            "segmentation": [[596, 207, 521, 201]],
            "iscrowd": 0,
        },
        {
            "id": 1,
            "image_id": 46,
            "category_id": 0,
            "segmentation": [[689, 787, 589, 745]],
            "iscrowd": 0,
        },
        {
            "id": 2,
            "image_id": 46,
            "category_id": 1,
            "segmentation": [[486, 335, 399, 102]],
            "iscrowd": 0,
        },
        {
            "id": 3,
            "image_id": 1,
            "category_id": 1,
            "segmentation": [[810, 225, 841, 234]],
            "iscrowd": 0,
        },
        {
            "id": 4,
            "image_id": 1,
            "category_id": 1,
            "segmentation": [[1070, 626, 1055, 722]],
            "iscrowd": 0,
        },
    ],
    "categories": [
        {
            "name": "crop: daucus carota",
            "common_name": "carrot",
            "species": "daucus carota",
            "eppo_taxon_code": "DAUCS",
            "eppo_nontaxon_code": "3UMRC",
            "role": "crop",
            "id": 0,
        },
        {
            "name": "weed: UNSPECIFIED",
            "species": "UNSPECIFIED",
            "role": "weed",
            "id": 1,
        },
    ],
    "info": {
        "description": "Cwfid annotations converted into WeedCOCO",
        "metadata": {
            "name": "Cwfid annotations converted into WeedCOCO",
            "description": "Carrots. All the carrots (and weeds).",
            "creator": [{"@type": "Person", "name": "Sebastian Haug"}],
            "datePublished": "2015-XX-XX",
            "license": "https://github.com/cwfid/dataset",
        },
    },
    "license": [
        {
            "id": 0,
            "url": "https://github.com/cwfid/dataset",
        }
    ],
    "agcontexts": [
        {
            "id": 0,
            "agcontext_name": "cwfid",
            "crop_type": "daucus carota",
            "bbch_growth_range": {"min": 10, "max": 20},
            "soil_colour": "grey",
            "surface_cover": "none",
            "surface_coverage": "0-25",
            "weather_description": "sunny",
            "location_lat": 53,
            "location_long": 11,
            "camera_make": "JAI AD-130GE",
            "camera_lens": "Fujinon TF15-DA-8",
            "camera_lens_focallength": 15,
            "camera_height": 450,
            "camera_angle": 90,
            "camera_fov": 22.6,
            "photography_description": "Mounted on boom",
            "ground_speed": 0,
            "lighting": "natural",
            "cropped_to_plant": False,
        }
    ],
}

test_missing_required_at_root_expected = [
    {
        "error_type": "jsonschema",
        "n_errors_found": "5",
        "error_details": [
            {
                "path": [],
                "value": {},
                "message": "'agcontexts' is a required property",
            },
            {
                "path": [],
                "value": {},
                "message": "'annotations' is a required property",
            },
            {
                "path": [],
                "value": {},
                "message": "'categories' is a required property",
            },
            {
                "path": [],
                "value": {},
                "message": "'info' is a required property",
            },
            {
                "path": [],
                "value": {},
                "message": "'images' is a required property",
            },
        ],
    },
    {
        "error_type": "jsonschema",
        "n_errors_found": "3",
        "error_details": [
            {
                "path": [],
                "value": {"images": [], "annotations": []},
                "message": "'agcontexts' is a required property",
            },
            {
                "path": [],
                "value": {"images": [], "annotations": []},
                "message": "'categories' is a required property",
            },
            {
                "path": [],
                "value": {"images": [], "annotations": []},
                "message": "'info' is a required property",
            },
        ],
    },
    {
        "error_type": "jsonschema",
        "n_errors_found": "2",
        "error_details": [
            {
                "path": [],
                "value": {"images": [], "annotations": [], "categories": []},
                "message": "'agcontexts' is a required property",
            },
            {
                "path": [],
                "value": {"images": [], "annotations": [], "categories": []},
                "message": "'info' is a required property",
            },
        ],
    },
]
