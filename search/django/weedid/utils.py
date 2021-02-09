import os
import json
from uuid import uuid4
from weedcoco.repo.deposit import mkdir_safely
from weedcoco.stats import WeedCOCOStats
from django.core.files.storage import FileSystemStorage
from weedid.models import Dataset, WeedidUser


def store_tmp_image(image, image_dir):
    fs = FileSystemStorage()
    fs.save(os.path.join(image_dir, image.name), image)


def store_tmp_weedcoco(weedcoco, upload_dir):
    fs = FileSystemStorage()
    weedcoco_path = os.path.join(upload_dir, weedcoco.name)
    fs.save(weedcoco_path, weedcoco)
    return weedcoco_path


def setup_upload_dir(upload_userid_dir):
    if not os.path.isdir(upload_userid_dir):
        mkdir_safely(upload_userid_dir)
    upload_id = str(uuid4())
    upload_dir = upload_userid_dir + f"/{upload_id}"
    mkdir_safely(upload_dir)
    return upload_dir, upload_id


def add_agcontexts(weedcoco_path, ag_contexts):
    with open(weedcoco_path, "r") as jsonFile:
        data = json.load(jsonFile)
    data["agcontexts"] = [ag_contexts]
    for image in data["images"]:
        image["agcontext_id"] = ag_contexts["id"]
    with open(weedcoco_path, "w") as jsonFile:
        json.dump(data, jsonFile)


def make_upload_entity_fields(weedcoco):
    category_to_name = {
        category["id"]: category["name"] for category in weedcoco["categories"]
    }

    stats = WeedCOCOStats(weedcoco)
    stats_with_cat_name = stats.category_summary.rename(
        index=category_to_name, level="category_id"
    )
    cat_counts_by_agcontext = dict(
        iter(stats_with_cat_name.groupby(level="agcontext_id"))
    )
    for agcontext in weedcoco["agcontexts"]:
        agcontext["n_images"] = stats.agcontext_summary.loc[agcontext["id"]].image_count

        # Should produce something like:
        # {"crop: daugus carota": {"image_count": 1, "annotation_count": 1, "bounding_box_count": 1, "segmentation_count": 1}}
        agcontext["category_statistics"] = cat_counts_by_agcontext[
            agcontext["id"]
        ].to_dict(orient="index")

    return {
        "agcontext": weedcoco["agcontexts"],
        "metadata": {
            "info": weedcoco["info"],
            "license": weedcoco["license"],
            "collections": weedcoco["collections"],
        },
    }


def create_upload_entity(weedcoco_path, upload_id, upload_userid):
    upload_user = WeedidUser.objects.get(id=upload_userid)

    with open(weedcoco_path) as f:
        weedcoco_json = json.load(f)
    fields = make_upload_entity_fields(weedcoco_json)

    upload_entity = Dataset(upload_id=upload_id, user=upload_user, status="N", **fields)
    upload_entity.save()
    upload_user.latest_upload = upload_entity
    upload_user.save()
