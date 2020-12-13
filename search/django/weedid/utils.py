import os
import re
import json
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
        os.mkdir(upload_userid_dir)
        latest_upload_dir_index = 0
    else:
        latest_upload_dir_index = max(
            [
                int(dir.split("_")[-1])
                for dir in os.listdir(upload_userid_dir)
                if re.fullmatch(r"^upload_\d+$", dir)
            ],
            default=0,
        )
    upload_dir = upload_userid_dir + f"/upload_{latest_upload_dir_index + 1}"
    os.mkdir(upload_dir)
    return upload_dir, f"upload_{latest_upload_dir_index + 1}"


def create_upload_entity(weedcoco_path, upload_id, upload_userid):
    upload_user = WeedidUser.objects.get(id=upload_userid)
    with open(weedcoco_path) as f:
        weedcoco_json = json.load(f)
    upload_entity = Dataset(
        upload_id=upload_id,
        upload_agcontext=weedcoco_json["agcontexts"],
        upload_user=upload_user,
        upload_status="N",
        metadata={
            "info": weedcoco_json["info"],
            "license": weedcoco_json["license"],
            "collections": weedcoco_json["collections"],
        },
    )
    upload_entity.save()
    upload_user.latest_upload = upload_entity
    upload_user.save()
