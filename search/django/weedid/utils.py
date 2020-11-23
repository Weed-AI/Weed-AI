import os
from django.core.files.storage import FileSystemStorage
import re


def store_tmp_image(image, image_dir):
    fs = FileSystemStorage()
    fs.save(os.path.join(image_dir, image.name), image)


def store_tmp_weedcoco(weedcoco, upload_dir):
    fs = FileSystemStorage()
    weedcoco_path = os.path.join(upload_dir, weedcoco.name)
    fs.save(weedcoco_path, weedcoco)
    return


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
