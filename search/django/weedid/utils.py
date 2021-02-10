import os
from shutil import rmtree
import json
from uuid import uuid4
from weedcoco.repo.deposit import mkdir_safely
from django.core.files.storage import FileSystemStorage
from weedid.models import Dataset, WeedidUser
from core.settings import UPLOAD_DIR, REPOSITORY_DIR, DOWNLOAD_DIR


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


def create_upload_entity(weedcoco_path, upload_id, upload_userid):
    upload_user = WeedidUser.objects.get(id=upload_userid)
    with open(weedcoco_path) as f:
        weedcoco_json = json.load(f)
    upload_entity = Dataset(
        upload_id=upload_id,
        agcontext=weedcoco_json["agcontexts"],
        user=upload_user,
        status="N",
        metadata={
            "info": weedcoco_json["info"],
            "license": weedcoco_json["license"],
            "collections": weedcoco_json["collections"],
        },
    )
    upload_entity.save()
    upload_user.latest_upload = upload_entity
    upload_user.save()


def remove_entity_local_record(user_id, upload_id):
    upload_dir_record = os.path.join(UPLOAD_DIR, user_id, upload_id)
    repository_dir_record = os.path.join(REPOSITORY_DIR, upload_id)
    download_dir_record = os.path.join(DOWNLOAD_DIR, f"{upload_id}.zip")
    for dir_path in [upload_dir_record, repository_dir_record, download_dir_record]:
        if os.path.isdir(dir_path):
            rmtree(dir_path, ignore_errors=True)
        elif os.path.isfile(dir_path):
            os.remove(dir_path)


def retrieve_listing_info(query_entity):
    """Retrieving info from specific upload entity"""
    return {
        "name": query_entity.metadata["info"][0]["name"]
        if "name" in query_entity.metadata["info"][0]
        else "",
        "upload_id": query_entity.upload_id,
        "upload_date": str(query_entity.date),
        "contributor": query_entity.user.username,
    }
