# import pathlib
# import json
# import pytest


# TEST_DATA_DIR = pathlib.Path(__file__).parent / "csv_data"
# AGCONTEXT = {
#     "bbch_growth_range": "na",
#     "camera_angle": 12,
#     "camera_fov": "variable",
#     "camera_height": 666,
#     "camera_lens": "dunno",
#     "camera_lens_focallength": 555,
#     "camera_make": "dunno",
#     "crop_type": "wheat",
#     "cropped_to_plant": False,
#     "id": 0,
#     "ground_speed": 0,
#     "lighting": "artificial",
#     "location_lat": 90,
#     "location_long": 90,
#     "photography_description": "foobar",
#     "soil_colour": "grey",
#     "surface_cover": "none",
#     "surface_coverage": "0-25",
#     "weather_description": "Nothing to note",
# }
# COMPLETE_WEEDCOCO = {
#     "agcontexts": [AGCONTEXT],
#     "annotations": [
#         {'image_id': 0, 'category_id': 0},
#         {'image_id': 0, 'category_id': 1},
#         {'image_id': 1, 'category_id': 0},
#     ],
#     "categories": [
#         {"id": 0, "name": "weed: lolium perenne"},
#         {"id": 1, "name": "weed: rapistrum rugosum"},
#     ],
#     "images": [
#         {'id': 0, 'file_name': '1.jpg'},
#         {'id': 1, 'file_name': '2.jpg'},
#     ],
#     "info": {},
# }
