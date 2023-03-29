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


DOUBTFUL_GENUS_WEEDCOCO = {
    "images": [
        {
            "id": 0,
            "folder": "C:\\Users\\gcol4791\\Downloads\\CottonWeedDet12\\weedImages",
            "file_name": "20210820_iPhoneSE_YL_1562.jpg",
            "width": 3024,
            "height": 4032,
            "depth": "3",
            "agcontext_id": 0,
        },
        {
            "id": 1,
            "folder": "C:\\Users\\gcol4791\\Downloads\\CottonWeedDet12\\weedImages",
            "file_name": "20210912_iPhoneSE_YL_76.jpg",
            "width": 3024,
            "height": 4032,
            "depth": "3",
            "agcontext_id": 0,
        },
    ],
    "annotations": [
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
    "categories": [
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
    "agcontexts": [
        {
            "id": 0,
            "crop_type": "daucus carota",
            "bbch_growth_range": {"min": 10, "max": 20},
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
            "photography_description": "Something",
            "weather_description": "Collected under all conditions, sunny, cloudy and overcast",
            "cropped_to_plant": False,
        }
    ],
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
