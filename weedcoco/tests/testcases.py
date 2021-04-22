MINIMAL_WEEDCOCO = {
    "images": [],
    "annotations": [],
    "categories": [],
    "agcontexts": [],
    "info": {
        "description": "Something",
        "metadata": {
            "name": "Something",
            "creator": [{"name": "Someone"}],
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
            "segmentation": [[596, 207, 521]],
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
            "segmentation": [[486, 335, 399]],
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
            "name": "weed: unspecified",
            "species": "UNSPECIFIED",
            "role": "weed",
            "id": 1,
        },
    ],
    "info": {
        "description": "Cwfid annotations converted into WeedCOCO",
        "metadata": {
            "name": "Cwfid annotations converted into WeedCOCO",
            "creator": [{"name": "Sebastian Haug"}],
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

test_bad_category_name_expected = [
    {
        "error_type": "jsonschema",
        "n_errors_found": "1",
        "error_details": [
            {
                "path": ["categories", 0, "name"],
                "value": "foobar",
                "message": "'foobar' does not match '^((crop|weed): ([a-z][a-z ]+|UNSPECIFIED)|crop|weed|none)$'",
                "schema": {
                    "type": "string",
                    "pattern": "^((crop|weed): ([a-z][a-z ]+|UNSPECIFIED)|crop|weed|none)$",
                    "description": 'A category for an annotation, consisting of an agricultural role and\noptionally a biological name, separated by ": ". Currently allowed\nagricultural roles are "weed" and "crop".  The "none" category may be\nused to indicate that no weed or crop is identified in the image.\n\nAnnotations should be labelled with the most specific category possible,\nusually "weed: <species name>", but super categories may be more general.\nBiological names should be lowercase.\nFor an unspecified species of weed, "weed: UNSPECIFIED" may be used.\n\nFor example, to label an oat crop in an image, the category name would be\n"crop: avena sativa". Its super categories may include "crop: grasses"\nand "crop". Oats as a volunteer crop would be "weed: avena sativa".',
                },
            }
        ],
    },
    {
        "error_type": "jsonschema",
        "n_errors_found": "1",
        "error_details": [
            {
                "path": ["categories", 0, "name"],
                "value": "weed: 1",
                "message": "'weed: 1' does not match '^((crop|weed): ([a-z][a-z ]+|UNSPECIFIED)|crop|weed|none)$'",
                "schema": {
                    "type": "string",
                    "pattern": "^((crop|weed): ([a-z][a-z ]+|UNSPECIFIED)|crop|weed|none)$",
                    "description": 'A category for an annotation, consisting of an agricultural role and\noptionally a biological name, separated by ": ". Currently allowed\nagricultural roles are "weed" and "crop".  The "none" category may be\nused to indicate that no weed or crop is identified in the image.\n\nAnnotations should be labelled with the most specific category possible,\nusually "weed: <species name>", but super categories may be more general.\nBiological names should be lowercase.\nFor an unspecified species of weed, "weed: UNSPECIFIED" may be used.\n\nFor example, to label an oat crop in an image, the category name would be\n"crop: avena sativa". Its super categories may include "crop: grasses"\nand "crop". Oats as a volunteer crop would be "weed: avena sativa".',
                },
            }
        ],
    },
]

test_missing_required_at_root_expected = [
    {
        "error_type": "jsonschema",
        "n_errors_found": "5",
        "error_details": [
            {
                "path": [],
                "value": {},
                "message": "'agcontexts' is a required property",
                "schema": {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "$id": "https://weedid.sydney.edu.au/schema/main.json",
                    "description": "Weed-COCO\nAn extension of MS COCO for Weed Identification in grain crops.\nMay also be applicable to related agricultural purposes.\n",
                    "type": "object",
                    "required": [
                        "agcontexts",
                        "annotations",
                        "categories",
                        "info",
                        "images",
                    ],
                    "properties": {
                        "images": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Image.json#/"
                            },
                        },
                        "annotations": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Annotation.json#/"
                            },
                        },
                        "categories": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Category.json#/"
                            },
                        },
                        "agcontexts": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/AgContext.json#/"
                            },
                        },
                        "info": {
                            "type": "object",
                            "required": ["description", "metadata"],
                            "properties": {
                                "description": {"type": "string"},
                                "contributor": {"type": "string"},
                                "url": {"type": "string"},
                                "version": {"type": "string"},
                                "date_created": {
                                    "type": "string",
                                    "format": "date-time",
                                },
                                "year": {"url": "string"},
                                "metadata": {
                                    "$ref": "https://weedid.sydney.edu.au/schema/Metadata.json#/"
                                },
                            },
                        },
                    },
                },
            },
            {
                "path": [],
                "value": {},
                "message": "'annotations' is a required property",
                "schema": {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "$id": "https://weedid.sydney.edu.au/schema/main.json",
                    "description": "Weed-COCO\nAn extension of MS COCO for Weed Identification in grain crops.\nMay also be applicable to related agricultural purposes.\n",
                    "type": "object",
                    "required": [
                        "agcontexts",
                        "annotations",
                        "categories",
                        "info",
                        "images",
                    ],
                    "properties": {
                        "images": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Image.json#/"
                            },
                        },
                        "annotations": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Annotation.json#/"
                            },
                        },
                        "categories": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Category.json#/"
                            },
                        },
                        "agcontexts": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/AgContext.json#/"
                            },
                        },
                        "info": {
                            "type": "object",
                            "required": ["description", "metadata"],
                            "properties": {
                                "description": {"type": "string"},
                                "contributor": {"type": "string"},
                                "url": {"type": "string"},
                                "version": {"type": "string"},
                                "date_created": {
                                    "type": "string",
                                    "format": "date-time",
                                },
                                "year": {"url": "string"},
                                "metadata": {
                                    "$ref": "https://weedid.sydney.edu.au/schema/Metadata.json#/"
                                },
                            },
                        },
                    },
                },
            },
            {
                "path": [],
                "value": {},
                "message": "'categories' is a required property",
                "schema": {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "$id": "https://weedid.sydney.edu.au/schema/main.json",
                    "description": "Weed-COCO\nAn extension of MS COCO for Weed Identification in grain crops.\nMay also be applicable to related agricultural purposes.\n",
                    "type": "object",
                    "required": [
                        "agcontexts",
                        "annotations",
                        "categories",
                        "info",
                        "images",
                    ],
                    "properties": {
                        "images": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Image.json#/"
                            },
                        },
                        "annotations": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Annotation.json#/"
                            },
                        },
                        "categories": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Category.json#/"
                            },
                        },
                        "agcontexts": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/AgContext.json#/"
                            },
                        },
                        "info": {
                            "type": "object",
                            "required": ["description", "metadata"],
                            "properties": {
                                "description": {"type": "string"},
                                "contributor": {"type": "string"},
                                "url": {"type": "string"},
                                "version": {"type": "string"},
                                "date_created": {
                                    "type": "string",
                                    "format": "date-time",
                                },
                                "year": {"url": "string"},
                                "metadata": {
                                    "$ref": "https://weedid.sydney.edu.au/schema/Metadata.json#/"
                                },
                            },
                        },
                    },
                },
            },
            {
                "path": [],
                "value": {},
                "message": "'info' is a required property",
                "schema": {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "$id": "https://weedid.sydney.edu.au/schema/main.json",
                    "description": "Weed-COCO\nAn extension of MS COCO for Weed Identification in grain crops.\nMay also be applicable to related agricultural purposes.\n",
                    "type": "object",
                    "required": [
                        "agcontexts",
                        "annotations",
                        "categories",
                        "info",
                        "images",
                    ],
                    "properties": {
                        "images": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Image.json#/"
                            },
                        },
                        "annotations": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Annotation.json#/"
                            },
                        },
                        "categories": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Category.json#/"
                            },
                        },
                        "agcontexts": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/AgContext.json#/"
                            },
                        },
                        "info": {
                            "type": "object",
                            "required": ["description", "metadata"],
                            "properties": {
                                "description": {"type": "string"},
                                "contributor": {"type": "string"},
                                "url": {"type": "string"},
                                "version": {"type": "string"},
                                "date_created": {
                                    "type": "string",
                                    "format": "date-time",
                                },
                                "year": {"url": "string"},
                                "metadata": {
                                    "$ref": "https://weedid.sydney.edu.au/schema/Metadata.json#/"
                                },
                            },
                        },
                    },
                },
            },
            {
                "path": [],
                "value": {},
                "message": "'images' is a required property",
                "schema": {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "$id": "https://weedid.sydney.edu.au/schema/main.json",
                    "description": "Weed-COCO\nAn extension of MS COCO for Weed Identification in grain crops.\nMay also be applicable to related agricultural purposes.\n",
                    "type": "object",
                    "required": [
                        "agcontexts",
                        "annotations",
                        "categories",
                        "info",
                        "images",
                    ],
                    "properties": {
                        "images": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Image.json#/"
                            },
                        },
                        "annotations": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Annotation.json#/"
                            },
                        },
                        "categories": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Category.json#/"
                            },
                        },
                        "agcontexts": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/AgContext.json#/"
                            },
                        },
                        "info": {
                            "type": "object",
                            "required": ["description", "metadata"],
                            "properties": {
                                "description": {"type": "string"},
                                "contributor": {"type": "string"},
                                "url": {"type": "string"},
                                "version": {"type": "string"},
                                "date_created": {
                                    "type": "string",
                                    "format": "date-time",
                                },
                                "year": {"url": "string"},
                                "metadata": {
                                    "$ref": "https://weedid.sydney.edu.au/schema/Metadata.json#/"
                                },
                            },
                        },
                    },
                },
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
                "schema": {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "$id": "https://weedid.sydney.edu.au/schema/main.json",
                    "description": "Weed-COCO\nAn extension of MS COCO for Weed Identification in grain crops.\nMay also be applicable to related agricultural purposes.\n",
                    "type": "object",
                    "required": [
                        "agcontexts",
                        "annotations",
                        "categories",
                        "info",
                        "images",
                    ],
                    "properties": {
                        "images": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Image.json#/"
                            },
                        },
                        "annotations": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Annotation.json#/"
                            },
                        },
                        "categories": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Category.json#/"
                            },
                        },
                        "agcontexts": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/AgContext.json#/"
                            },
                        },
                        "info": {
                            "type": "object",
                            "required": ["description", "metadata"],
                            "properties": {
                                "description": {"type": "string"},
                                "contributor": {"type": "string"},
                                "url": {"type": "string"},
                                "version": {"type": "string"},
                                "date_created": {
                                    "type": "string",
                                    "format": "date-time",
                                },
                                "year": {"url": "string"},
                                "metadata": {
                                    "$ref": "https://weedid.sydney.edu.au/schema/Metadata.json#/"
                                },
                            },
                        },
                    },
                },
            },
            {
                "path": [],
                "value": {"images": [], "annotations": []},
                "message": "'categories' is a required property",
                "schema": {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "$id": "https://weedid.sydney.edu.au/schema/main.json",
                    "description": "Weed-COCO\nAn extension of MS COCO for Weed Identification in grain crops.\nMay also be applicable to related agricultural purposes.\n",
                    "type": "object",
                    "required": [
                        "agcontexts",
                        "annotations",
                        "categories",
                        "info",
                        "images",
                    ],
                    "properties": {
                        "images": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Image.json#/"
                            },
                        },
                        "annotations": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Annotation.json#/"
                            },
                        },
                        "categories": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Category.json#/"
                            },
                        },
                        "agcontexts": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/AgContext.json#/"
                            },
                        },
                        "info": {
                            "type": "object",
                            "required": ["description", "metadata"],
                            "properties": {
                                "description": {"type": "string"},
                                "contributor": {"type": "string"},
                                "url": {"type": "string"},
                                "version": {"type": "string"},
                                "date_created": {
                                    "type": "string",
                                    "format": "date-time",
                                },
                                "year": {"url": "string"},
                                "metadata": {
                                    "$ref": "https://weedid.sydney.edu.au/schema/Metadata.json#/"
                                },
                            },
                        },
                    },
                },
            },
            {
                "path": [],
                "value": {"images": [], "annotations": []},
                "message": "'info' is a required property",
                "schema": {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "$id": "https://weedid.sydney.edu.au/schema/main.json",
                    "description": "Weed-COCO\nAn extension of MS COCO for Weed Identification in grain crops.\nMay also be applicable to related agricultural purposes.\n",
                    "type": "object",
                    "required": [
                        "agcontexts",
                        "annotations",
                        "categories",
                        "info",
                        "images",
                    ],
                    "properties": {
                        "images": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Image.json#/"
                            },
                        },
                        "annotations": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Annotation.json#/"
                            },
                        },
                        "categories": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Category.json#/"
                            },
                        },
                        "agcontexts": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/AgContext.json#/"
                            },
                        },
                        "info": {
                            "type": "object",
                            "required": ["description", "metadata"],
                            "properties": {
                                "description": {"type": "string"},
                                "contributor": {"type": "string"},
                                "url": {"type": "string"},
                                "version": {"type": "string"},
                                "date_created": {
                                    "type": "string",
                                    "format": "date-time",
                                },
                                "year": {"url": "string"},
                                "metadata": {
                                    "$ref": "https://weedid.sydney.edu.au/schema/Metadata.json#/"
                                },
                            },
                        },
                    },
                },
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
                "schema": {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "$id": "https://weedid.sydney.edu.au/schema/main.json",
                    "description": "Weed-COCO\nAn extension of MS COCO for Weed Identification in grain crops.\nMay also be applicable to related agricultural purposes.\n",
                    "type": "object",
                    "required": [
                        "agcontexts",
                        "annotations",
                        "categories",
                        "info",
                        "images",
                    ],
                    "properties": {
                        "images": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Image.json#/"
                            },
                        },
                        "annotations": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Annotation.json#/"
                            },
                        },
                        "categories": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Category.json#/"
                            },
                        },
                        "agcontexts": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/AgContext.json#/"
                            },
                        },
                        "info": {
                            "type": "object",
                            "required": ["description", "metadata"],
                            "properties": {
                                "description": {"type": "string"},
                                "contributor": {"type": "string"},
                                "url": {"type": "string"},
                                "version": {"type": "string"},
                                "date_created": {
                                    "type": "string",
                                    "format": "date-time",
                                },
                                "year": {"url": "string"},
                                "metadata": {
                                    "$ref": "https://weedid.sydney.edu.au/schema/Metadata.json#/"
                                },
                            },
                        },
                    },
                },
            },
            {
                "path": [],
                "value": {"images": [], "annotations": [], "categories": []},
                "message": "'info' is a required property",
                "schema": {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "$id": "https://weedid.sydney.edu.au/schema/main.json",
                    "description": "Weed-COCO\nAn extension of MS COCO for Weed Identification in grain crops.\nMay also be applicable to related agricultural purposes.\n",
                    "type": "object",
                    "required": [
                        "agcontexts",
                        "annotations",
                        "categories",
                        "info",
                        "images",
                    ],
                    "properties": {
                        "images": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Image.json#/"
                            },
                        },
                        "annotations": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Annotation.json#/"
                            },
                        },
                        "categories": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/Category.json#/"
                            },
                        },
                        "agcontexts": {
                            "type": "array",
                            "items": {
                                "$ref": "https://weedid.sydney.edu.au/schema/AgContext.json#/"
                            },
                        },
                        "info": {
                            "type": "object",
                            "required": ["description", "metadata"],
                            "properties": {
                                "description": {"type": "string"},
                                "contributor": {"type": "string"},
                                "url": {"type": "string"},
                                "version": {"type": "string"},
                                "date_created": {
                                    "type": "string",
                                    "format": "date-time",
                                },
                                "year": {"url": "string"},
                                "metadata": {
                                    "$ref": "https://weedid.sydney.edu.au/schema/Metadata.json#/"
                                },
                            },
                        },
                    },
                },
            },
        ],
    },
]
