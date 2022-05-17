import json
import os
import re
import smtplib
from email.message import EmailMessage
from shutil import move, rmtree
from uuid import uuid4

from core.settings import (
    DOWNLOAD_DIR,
    FROM_EMAIL,
    REPOSITORY_DIR,
    SEND_EMAIL,
    SMTP_HOST,
    SMTP_PORT,
    UPLOAD_DIR,
)
from django.core.files.storage import FileSystemStorage
from weedcoco.repo.deposit import Repository, mkdir_safely
from weedcoco.stats import WeedCOCOStats
from weedcoco.utils import copy_without_exif, set_info, set_licenses
from weedcoco.validation import validate

from weedid.models import Dataset, WeedidUser


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(name)
        return name


def store_tmp_image(image, image_dir):
    fs = OverwriteStorage()
    image_file = os.path.join(image_dir, image.name)
    fs.save(image_file, image)
    copy_without_exif(image_file, image_file)


def store_tmp_weedcoco(weedcoco, upload_dir):
    weedcoco_path = os.path.join(upload_dir, "weedcoco.json")
    if os.path.isfile(weedcoco_path):
        os.remove(weedcoco_path)
    with open(weedcoco_path, "w") as weedcoco_file:
        weedcoco_file.write(json.dumps(weedcoco))


def store_tmp_voc(voc, voc_dir):
    fs = OverwriteStorage()
    fs.save(os.path.join(voc_dir, voc.name), voc)


def move_to_upload(store_dir, upload_dir, mode=""):
    move(store_dir, os.path.join(upload_dir, mode))


def setup_upload_dir(upload_userid_dir):
    if not os.path.isdir(upload_userid_dir):
        mkdir_safely(upload_userid_dir)
    upload_id = str(str(uuid4()))
    upload_dir = os.path.join(upload_userid_dir, upload_id)
    mkdir_safely(upload_dir)
    return upload_dir, upload_id


def set_categories(weedcoco_path, categories):
    with open(weedcoco_path, "r") as jsonFile:
        data = json.load(jsonFile)
    new_categories = []
    for category in categories:
        if category["role"] and category["scientific_name"]:
            new_categories.append(
                {
                    "id": category["id"],
                    "name": ": ".join((category["role"], category["scientific_name"])),
                }
            )
        else:
            new_categories.append({"id": category["id"], "name": category["name"]})
    data["categories"] = new_categories
    with open(weedcoco_path, "w") as jsonFile:
        json.dump(data, jsonFile)
    return data


def add_agcontexts(weedcoco_path, ag_contexts):
    with open(weedcoco_path, "r") as jsonFile:
        data = json.load(jsonFile)
    data["agcontexts"] = [ag_contexts]
    for image in data["images"]:
        image["agcontext_id"] = ag_contexts["id"]
    with open(weedcoco_path, "w") as jsonFile:
        json.dump(data, jsonFile)


def add_metadata(weedcoco_path, metadata):
    with open(weedcoco_path, "r") as jsonFile:
        data = json.load(jsonFile)
    set_info(data, metadata)
    set_licenses(data)
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
        agcontext["n_images"] = int(
            stats.agcontext_summary.loc[agcontext["id"]].image_count
        ) + count_image_with_no_annotation(weedcoco)

        # Should produce something like:
        # {"crop: daucus carota": {"image_count": 1, "annotation_count": 1, "bounding_box_count": 1, "segmentation_count": 1}}
        # XXX: we use json.loads and to_json instead of to_dict, since to_dict
        #      was returning numpy.int64 numbers that could not be serialised.
        agcontext["category_statistics"] = json.loads(
            cat_counts_by_agcontext[agcontext["id"]]
            .droplevel("agcontext_id")
            .to_json(orient="index")
        )

    return {
        "agcontext": weedcoco["agcontexts"],
        "metadata": weedcoco["info"]["metadata"],
    }


def count_image_with_no_annotation(weedcoco):
    return len(
        set([image["id"] for image in weedcoco["images"]])
        - set([annotation["image_id"] for annotation in weedcoco["annotations"]])
    )


def create_upload_entity(upload_id, upload_userid):
    upload_user = WeedidUser.objects.get(id=upload_userid)
    upload_entity = Dataset(upload_id=upload_id, user=upload_user, status="N")
    upload_entity.save()
    upload_user.latest_upload = upload_entity
    upload_user.save()


def remove_entity_local_record(user_id, upload_id):
    upload_dir_record = os.path.join(UPLOAD_DIR, user_id, upload_id)
    repository = Repository(REPOSITORY_DIR)
    dataset = repository.dataset(upload_id)
    repository_dir_record = dataset.object_path
    download_dir_record = os.path.join(DOWNLOAD_DIR, f"{upload_id}.zip")
    for dir_path in [upload_dir_record, repository_dir_record, download_dir_record]:
        if os.path.isdir(dir_path):
            rmtree(dir_path, ignore_errors=True)
        elif os.path.isfile(dir_path):
            os.remove(dir_path)


def retrieve_listing_info(query_entity, awaiting_review, user_id=0):
    """Retrieving info from specific upload entity"""
    return {
        "name": query_entity.metadata["name"]
        if "name" in query_entity.metadata
        else "",
        "upload_id": query_entity.upload_id,
        "upload_date": str(query_entity.date),
        "contributor": query_entity.user.username,
        "contributor_email": query_entity.user.email if awaiting_review else "",
        "editable": query_entity.user.id == user_id,
    }


def validate_email_format(email):
    regex = "^(\\w|\\.|\\_|\\-)+[@](\\w|\\_|\\-|\\.)+[.]\\w{2,3}$"
    return re.fullmatch(regex, email)


def send_email(subject, body, recipients):
    if SEND_EMAIL and SMTP_HOST and SMTP_PORT:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            for recipient in recipients:
                msg = EmailMessage()
                msg["Subject"], msg["From"], msg["To"] = subject, FROM_EMAIL, recipient
                msg.set_content(body)
                smtp.send_message(msg)


def parse_category_name(category):
    if re.fullmatch(r"(crop|weed): .+", category["name"]):
        return {
            "id": category["id"],
            "name": category["name"],
            "role": category["name"].split(": ", maxsplit=1)[0],
            "scientific_name": category["name"].split(": ", maxsplit=1)[1],
        }
    else:
        return {
            "id": category["id"],
            "name": category["name"],
            "role": "",
            "scientific_name": "",
        }


def retrieve_missing_images_list(weedcoco_json, images_path, upload_id):
    current_images = []
    for image_reference in weedcoco_json["images"]:
        current_images.append(image_reference["file_name"].split("/")[-1])
    if not os.path.isdir(images_path):
        mkdir_safely(images_path)
        return current_images[:]
    existing_images = set(os.listdir(images_path))
    return [image for image in current_images if image not in existing_images]


def upload_helper(weedcoco_json, user_id, schema="coco", upload_id=None):
    images = []
    validate(
        weedcoco_json,
        schema=schema,
    )
    categories = [
        parse_category_name(category) for category in weedcoco_json["categories"]
    ]
    if not upload_id or len(upload_id) != len(str(uuid4())):
        upload_dir, upload_id = setup_upload_dir(os.path.join(UPLOAD_DIR, str(user_id)))
        create_upload_entity(upload_id, user_id)
    else:
        upload_dir = os.path.join(UPLOAD_DIR, str(user_id), upload_id)
    images = retrieve_missing_images_list(
        weedcoco_json, os.path.join(upload_dir, "images"), upload_id
    )
    store_tmp_weedcoco(weedcoco_json, upload_dir)
    return upload_id, images, categories
