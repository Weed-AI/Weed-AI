from django.http import HttpResponse
from django.shortcuts import render

import requests
import os
import json
import traceback
import shutil

from core.settings import (
    UPLOAD_DIR,
    TUS_DESTINATION_DIR,
    REPOSITORY_DIR,
    CVAT_DATA_DIR,
    MAX_IMAGE_SIZE,
    MAX_VOC_SIZE,
    SITE_BASE_URL,
)
from weedid.tasks import submit_upload_task, update_index_and_thumbnails
from weedid.utils import (
    store_tmp_weedcoco,
    setup_upload_dir,
    store_tmp_image,
    store_tmp_image_from_zip,
    store_tmp_voc,
    move_to_upload,
    create_upload_entity,
    retrieve_listing_info,
    remove_entity_local_record,
    set_categories,
    add_agcontexts,
    add_metadata,
    validate_email_format,
    parse_category_name,
)
from weedid.notification import review_notification
from weedid.models import Dataset, WeedidUser
from weedcoco.validation import (
    validate,
    validate_json,
    JsonValidationError,
)
from weedcoco.importers.voc import voc_to_coco
from weedcoco.importers.mask import masks_to_coco, generate_paths_from_mask_only
from weedcoco.repo.deposit import mkdir_safely
from weedcoco.utils import fix_compatibility_quirks
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.http import (
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    HttpResponseBadRequest,
    HttpResponseServerError,
)
from django.views.decorators.csrf import ensure_csrf_cookie
from pathlib import Path
from zipfile import ZipFile

import logging

logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def set_csrf(request):
    return HttpResponse("Success")


def json_validation_response(exc):
    return HttpResponseBadRequest(
        json.dumps(exc.get_error_details()), content_type="application/json"
    )


def elasticsearch_query(request):
    try:
        elasticsearch_url = "/".join(request.path.split("/")[2:])
    except Exception:
        return HttpResponseBadRequest("Invalid query format")
    if not elasticsearch_url.startswith("weedid/_msearch"):
        return HttpResponseBadRequest("Only _msearch queries are currently forwarded")
    if request.method not in ["POST", "GET"]:
        return HttpResponseNotAllowed(request.method)
    elasticsearch_response = requests.post(
        url=f"http://elasticsearch:9200/{elasticsearch_url}",
        data=request.body,
        headers=request.headers,
    )
    return HttpResponse(elasticsearch_response)


def upload_helper(weedcoco_json, user_id, schema="coco"):
    images = []
    validate(
        weedcoco_json,
        schema=schema,
    )
    for image_reference in weedcoco_json["images"]:
        images.append(image_reference["file_name"].split("/")[-1])
    categories = [
        parse_category_name(category) for category in weedcoco_json["categories"]
    ]
    upload_dir, upload_id = setup_upload_dir(os.path.join(UPLOAD_DIR, str(user_id)))
    store_tmp_weedcoco(weedcoco_json, upload_dir)
    create_upload_entity(upload_id, user_id)
    return upload_id, images, categories


def upload(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(request.method)
    user = request.user
    if not (user and user.is_authenticated):
        return HttpResponseForbidden("You dont have access to proceed")
    try:
        images = []
        file_weedcoco = request.FILES["weedcoco"]
        weedcoco_json = json.load(file_weedcoco)
        fix_compatibility_quirks(weedcoco_json)
        upload_id, images, categories = upload_helper(
            weedcoco_json, user.id, request.POST["schema"]
        )
    except JsonValidationError as e:
        traceback.print_exc()
        return json_validation_response(e)
    except Exception as e:
        traceback.print_exc()
        return HttpResponseBadRequest(str(e))
    else:
        return HttpResponse(
            json.dumps(
                {"upload_id": upload_id, "images": images, "categories": categories}
            )
        )


def retrieve_cvat_task(request, task_id):
    user = request.user
    if not (user and user.is_authenticated):
        return HttpResponseForbidden("You dont have access to proceed")
    try:
        with ZipFile(
            os.path.join(
                CVAT_DATA_DIR, "tasks", task_id, "export_cache/annotations_coco-10.ZIP"
            )
        ) as cvat_zip:
            with cvat_zip.open("annotations/instances_default.json") as cvat_task_coco:
                coco_json = json.load(cvat_task_coco)
                upload_id, images, categories = upload_helper(coco_json, user.id)
    except JsonValidationError as e:
        traceback.print_exc()
        return json_validation_response(e)
    except Exception as e:
        traceback.print_exc()
        return HttpResponseBadRequest(str(e))
    else:
        return HttpResponse(
            json.dumps(
                {"upload_id": upload_id, "images": images, "categories": categories}
            )
        )


class CustomUploader:
    @classmethod
    def upload(cls, request):
        if not request.method == "POST":
            return HttpResponseNotAllowed(request.method)
        user = request.user
        if not (user and user.is_authenticated):
            return HttpResponseForbidden("You dont have access to proceed")
        try:
            store_id = request.POST[cls.id_name]
            if "/" in store_id:
                return HttpResponseBadRequest("Bad id")
            payload = request.FILES[cls.payload_name]
            if payload.size > cls.max_file_size:
                return HttpResponseBadRequest(
                    f"This file has exceeded the size limit {cls.max_file_size} Byte!"
                )
            store_dir = os.path.join(UPLOAD_DIR, str(user.id), store_id)
            cls.store_tmp(payload, store_dir)
        except Exception as e:
            traceback.print_exc()
            return HttpResponseBadRequest(str(e))
        else:
            return HttpResponse(f"Uploaded {payload.name} to {store_dir}")

    @classmethod
    def remove(cls, request):
        if not request.method == "POST":
            return HttpResponseNotAllowed(request.method)
        user = request.user
        if not (user and user.is_authenticated):
            return HttpResponseForbidden("You dont have access to proceed")
        try:
            store_id = request.POST[cls.id_name]
            if "/" in store_id:
                return HttpResponseBadRequest("Bad id")
            remove_name = request.POST[cls.remove_name]
            file_to_remove = os.path.join(
                UPLOAD_DIR, str(user.id), store_id, remove_name
            )
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)
                return HttpResponse(f"Removed {remove_name}")
            else:
                return HttpResponse(f"{remove_name} doesn't exist")
        except Exception:
            return HttpResponseBadRequest(f"Error when removing {remove_name}")

    @classmethod
    def move(cls, request):
        if not request.method == "POST":
            return HttpResponseNotAllowed(request.method)
        user = request.user
        if not (user and user.is_authenticated):
            return HttpResponseForbidden("You dont have access to proceed")
        try:
            store_id = request.POST[cls.id_name]
            if "/" in store_id:
                return HttpResponseBadRequest("Bad id")
            upload_id = request.POST["upload_id"]
            store_dir = os.path.join(UPLOAD_DIR, str(user.id), store_id)
            upload_dir = os.path.join(UPLOAD_DIR, str(user.id), upload_id)
            move_to_upload(store_dir, upload_dir, cls.mode)
            return HttpResponse(
                f"{cls.mode} files of {store_id} has been moved to {upload_dir}"
            )
        except Exception as e:
            return HttpResponseBadRequest(str(e))

    @classmethod
    def submit(cls, request):
        if not request.method == "POST":
            return HttpResponseNotAllowed(request.method)
        user = request.user
        if not (user and user.is_authenticated):
            return HttpResponseForbidden("You dont have access to proceed")
        try:
            store_id = request.POST[cls.id_name]
            if "/" in store_id:
                return HttpResponseBadRequest("Bad id")
            images = []
            coco_json = cls.convert_to_coco(
                Path(os.path.join(UPLOAD_DIR, str(user.id), store_id)), request
            )
            validate(coco_json, schema="coco")
            fix_compatibility_quirks(coco_json)
            for image_reference in coco_json["images"]:
                images.append(image_reference["file_name"].split("/")[-1])
            categories = [
                parse_category_name(category) for category in coco_json["categories"]
            ]
            upload_dir, upload_id = setup_upload_dir(
                os.path.join(UPLOAD_DIR, str(user.id))
            )
            store_tmp_weedcoco(coco_json, upload_dir)
            create_upload_entity(upload_id, user.id)
        except JsonValidationError as e:
            traceback.print_exc()
            return json_validation_response(e)
        except Exception as e:
            traceback.print_exc()
            return HttpResponseBadRequest(str(e))
        else:
            return HttpResponse(
                json.dumps(
                    {"upload_id": upload_id, "images": images, "categories": categories}
                )
            )


class VocUploader(CustomUploader):
    mode = "voc"
    id_name = "voc_id"
    payload_name = "voc"
    remove_name = "voc_name"
    max_file_size = MAX_VOC_SIZE
    store_tmp = store_tmp_voc

    @staticmethod
    def convert_to_coco(store_path, request):
        return voc_to_coco(store_path)


class MaskUploader(CustomUploader):
    mode = "masks"
    id_name = "mask_id"
    payload_name = "upload_image"
    remove_name = "image_name"
    max_file_size = MAX_IMAGE_SIZE
    store_tmp = store_tmp_image

    @staticmethod
    def convert_to_coco(store_path, request):
        image_ext = request.POST["image_ext"]
        return masks_to_coco(
            generate_paths_from_mask_only(store_path, image_ext),
            background_if_unmapped="000000",
            check_consistent_dimensions=False,
        )


def upload_image(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(request.method)
    user = request.user
    if not (user and user.is_authenticated):
        return HttpResponseForbidden("You dont have access to proceed")
    upload_id = request.POST["upload_id"]
    upload_image = request.FILES["upload_image"]
    if upload_image.size > MAX_IMAGE_SIZE:
        return HttpResponseBadRequest("This image has exceeded the size limit!")
    upload_dir = os.path.join(UPLOAD_DIR, str(user.id), upload_id, "images")
    store_tmp_image(upload_image, upload_dir)
    return HttpResponse(f"Uploaded {upload_image.name} to {upload_dir}")


def unpack_image_zip(request):
    """Unpack a zipfile which has been uploaded via tus"""
    if not request.method == "POST":
        return HttpResponseNotAllowed(request.method)
    user = request.user
    if not (user and user.is_authenticated):
        return HttpResponseForbidden("You dont have access to proceed")
    upload_id = request.POST["upload_id"]
    upload_image_zip = request.POST["upload_image_zip"]
    # Get list of missing images from frontend to calculate images that are still missing after the current zip being uploaded
    images = request.POST["images"].split(",")
    zipfile = os.path.join(TUS_DESTINATION_DIR, upload_image_zip)
    upload_dir = os.path.join(UPLOAD_DIR, str(user.id), upload_id, "images")
    try:
        missing_images = store_tmp_image_from_zip(zipfile, upload_dir, images)
    except Exception as e:
        return HttpResponseBadRequest(str(e))
    return HttpResponse(
        json.dumps({"upload_id": upload_id, "missing_images": missing_images})
    )


def update_categories(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(request.method)
    user = request.user
    if not (user and user.is_authenticated):
        return HttpResponseForbidden("You dont have access to proceed")
    data = json.loads(request.body)
    upload_id, categories = data["upload_id"], data["categories"]
    weedcoco_path = os.path.join(
        UPLOAD_DIR, str(user.id), str(upload_id), "weedcoco.json"
    )
    try:
        updated_weedcoco_json = set_categories(weedcoco_path, categories)
        validate_json(updated_weedcoco_json, schema="compatible-coco")
    except JsonValidationError as e:
        traceback.print_exc()
        return json_validation_response(e)
    except Exception as e:
        traceback.print_exc()
        return HttpResponseBadRequest(str(e))
    else:
        return HttpResponse(
            f"Updated categories for user {user.id}'s upload{upload_id}"
        )


def upload_agcontexts(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(request.method)
    user = request.user
    if not (user and user.is_authenticated):
        return HttpResponseForbidden("You dont have access to proceed")
    data = json.loads(request.body)
    upload_id, ag_contexts = data["upload_id"], data["ag_contexts"]
    try:
        validate_json(ag_contexts, schema="agcontext")
    except JsonValidationError as e:
        traceback.print_exc()
        return json_validation_response(e)
    weedcoco_path = os.path.join(
        UPLOAD_DIR, str(user.id), str(upload_id), "weedcoco.json"
    )
    try:
        add_agcontexts(weedcoco_path, ag_contexts)
        Dataset.objects.filter(upload_id=upload_id).update(agcontext=[ag_contexts])
    except Exception:
        return HttpResponseNotAllowed("Failed to add AgContexts")
    else:
        return HttpResponse(
            f"Updated AgContexts for user {user.id}'s upload{upload_id}"
        )


def upload_metadata(request):
    if request.method == "POST":
        user = request.user
        if user and user.is_authenticated:
            data = json.loads(request.body)
            upload_id, metadata = data["upload_id"], data["metadata"]
            try:
                validate_json(metadata, schema="metadata")
            except JsonValidationError as e:
                traceback.print_exc()
                return json_validation_response(e)
            weedcoco_path = os.path.join(
                UPLOAD_DIR, str(user.id), str(upload_id), "weedcoco.json"
            )
            try:
                add_metadata(weedcoco_path, metadata)
                Dataset.objects.filter(upload_id=upload_id).update(metadata=metadata)
            except Exception:
                return HttpResponseNotAllowed("Failed to add Metadata")
            else:
                return HttpResponse(
                    f"Updated Metadata for user {user.id}'s upload{upload_id}"
                )
        else:
            return HttpResponseForbidden("You dont have access to proceed")
    else:
        return HttpResponseNotAllowed(request.method)


def copy_cvat(request):
    """Copy the images for a CVAT task from the CVAT volume to the upload dir"""
    if not request.method == "POST":
        return HttpResponseNotAllowed(request.method)
    user = request.user
    if not (user and user.is_authenticated):
        return HttpResponseForbidden("You dont have access to proceed")
    upload_id = request.POST["upload_id"]
    cvat_task_id = request.POST["task_id"]
    upload_dir = os.path.join(UPLOAD_DIR, str(user.id), str(upload_id))
    if not os.path.isdir(upload_dir):
        return HttpResponseServerError(f"upload directory {upload_id} not found")
    image_dir = os.path.join(upload_dir, "images")
    if not os.path.isdir(image_dir):
        mkdir_safely(image_dir)
    weedcoco_path = os.path.join(upload_dir, "weedcoco.json")
    try:
        with open(weedcoco_path, "r") as weedcoco_file:
            weedcoco = json.load(weedcoco_file)
            missing = []
            for img in weedcoco["images"]:
                fn = img["file_name"]
                cvat_image = os.path.join(
                    CVAT_DATA_DIR, "data", str(cvat_task_id), "raw", fn
                )
                weedai_image = os.path.join(image_dir, fn)
                logger.warn(f"copy {cvat_image} -> {weedai_image}")
                try:
                    shutil.copy(cvat_image, weedai_image)
                except Exception as e:
                    logger.error(f"error copying {cvat_image} to {weedai_image}: {e}")
                    missing.append(img["image_id"])
            return HttpResponse(
                json.dumps({"upload_id": upload_id, "missing_images": missing})
            )
    except Exception as e:
        logger.error(f"error copying files: {e}")
        return HttpResponseServerError(f"error copying files: {e}")


def submit_deposit(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(request.method)
    user = request.user
    if not (user and user.is_authenticated):
        return HttpResponseForbidden("You dont have access to proceed")
    upload_id = request.POST["upload_id"]
    weedcoco_path = os.path.join(
        UPLOAD_DIR, str(user.id), str(upload_id), "weedcoco.json"
    )
    images_dir = os.path.join(UPLOAD_DIR, str(user.id), str(upload_id), "images")
    submit_upload_task.delay(weedcoco_path, images_dir, upload_id)
    return HttpResponse(f"Work on user {user.id}'s upload{upload_id}")


def upload_status(request):
    user = request.user
    if not (user and user.is_authenticated):
        return HttpResponse("You havent been logged in")
    user_id = request.user.id
    upload_entity = WeedidUser.objects.get(id=user_id).latest_upload
    return HttpResponse(
        json.dumps(
            {
                "upload_status": upload_entity.status,
                "upload_status_details": upload_entity.status_details,
            }
        )
    )


def upload_info(request, dataset_id):
    if request.method != "GET":
        return HttpResponseNotAllowed(request.method)
    upload_entity = Dataset.objects.get(upload_id=dataset_id)
    return HttpResponse(
        json.dumps(
            {"metadata": upload_entity.metadata, "agcontexts": upload_entity.agcontext}
        )
    )


def upload_list(request):
    upload_list = [
        retrieve_listing_info(dataset, awaiting_review=False)
        for dataset in Dataset.objects.filter(status="C")
    ]
    return HttpResponse(json.dumps(upload_list))


def awaiting_list(request):
    user = request.user
    if not (user and user.is_authenticated and user.is_staff):
        return HttpResponseForbidden("You dont have access to proceed")
    try:
        awaiting_list = [
            retrieve_listing_info(dataset, awaiting_review=True)
            for dataset in Dataset.objects.filter(status="AR")
        ]
        return HttpResponse(json.dumps(awaiting_list))
    except Exception:
        return HttpResponseNotAllowed("Awaiting list is not able to retrieve")


def editing_list(request):
    user = request.user
    if not (user and user.is_authenticated):
        return HttpResponseForbidden("You dont have access to proceed")
    try:
        editing_list = [
            retrieve_listing_info(dataset, awaiting_review=False)
            for dataset in Dataset.objects.filter(status="C", user=WeedidUser.objects.get(id=user.id))
        ]
        return HttpResponse(json.dumps(editing_list))
    except Exception:
        return HttpResponseNotAllowed("There is no dataset to edit for this user")

def dataset_approve(request, dataset_id):
    user = request.user
    if not (user and dataset_id and user.is_authenticated and user.is_staff):
        return HttpResponseForbidden("You dont have access to proceed")
    upload_entity = Dataset.objects.get(upload_id=dataset_id, status="AR")
    if upload_entity:
        weedcoco_path = os.path.join(REPOSITORY_DIR, str(dataset_id), "weedcoco.json")
        update_index_and_thumbnails.delay(weedcoco_path, dataset_id)
        upload_entity.status = "P"
        upload_entity.status_details = "It's now being indexed"
        upload_entity.save()
        return HttpResponse("It has been sent to be indexed")
    else:
        return HttpResponseNotAllowed("Dataset to be reviewed doesn't exist")


def dataset_reject(request, dataset_id):
    user = request.user
    if not (user and dataset_id and user.is_authenticated and user.is_staff):
        return HttpResponseForbidden("You dont have access to proceed")
    upload_entity = Dataset.objects.get(upload_id=dataset_id, status="AR")
    if upload_entity:
        try:
            remove_entity_local_record(str(upload_entity.user_id), str(dataset_id))
        finally:
            upload_entity.status = "F"
            upload_entity.status_details = "It failed to proceed after review."
            upload_entity.save()
            review_notification("rejected", dataset_id)
        return HttpResponse("The dataset has been rejected and removed")
    else:
        return HttpResponseNotAllowed("Dataset to be rejected doesn't exist")


def user_register(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(request.method)
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    if WeedidUser.objects.filter(username=username).count():
        return HttpResponseBadRequest("Username already exists")
    if WeedidUser.objects.filter(email=email).count():
        return HttpResponseBadRequest("Email already exists")
    if not validate_email_format(email):
        return HttpResponseBadRequest("Invalid email format")
    try:
        user = WeedidUser.objects.create_user(username, email, password)
        user.save()
        return HttpResponse("The account has been created")
    except Exception:
        return HttpResponseServerError("Server error")


def user_login(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(request.method)
    username = request.POST["username"]
    password = request.POST["password"]
    if not WeedidUser.objects.filter(username=username).count():
        return HttpResponseBadRequest("Username doesn't exist")
    user = WeedidUser.objects.get(username=username)
    if user is not None and not (
        user.password == password or check_password(password, user.password)
    ):
        return HttpResponseBadRequest("Incorrect credentials")
    else:
        try:
            login(request, user)
            return HttpResponse("You have been logged in")
        except Exception:
            return HttpResponseServerError("Server error")


def user_logout(request):
    logout(request)
    return HttpResponse("You have been logged out")


def user_login_status(request):
    if request.user.is_authenticated:
        return HttpResponse("You have been logged in")
    else:
        return HttpResponseForbidden("You havent been logged in")


def login_google(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(request.method)
    body = json.loads(request.body)
    email, googleId = body["email"], body["googleId"]
    users = WeedidUser.objects.all().filter(email=email)
    if len(users) > 0:
        login(request, users[0])
        return HttpResponse("You have been logged in")
    else:
        user = WeedidUser.objects.create_user(email.split("@")[0], email, googleId)
        user.save()
        login(request, user)
        return HttpResponse("The account has been created and logged in")


def sitemap_xml(request):
    # roughly in order of SEO importance
    PATHS = [
        "/explore",
        "/datasets",
        "/editor",
        "/upload",
        "/about",
        "/weedcoco",
        "/meta-editor",
    ]
    urls = [{"loc": SITE_BASE_URL + path} for path in PATHS]
    for dataset in Dataset.objects.filter(status="C"):
        urls.append({"loc": SITE_BASE_URL + "/datasets/" + dataset.upload_id})
    return render(
        request, "sitemap.xml", context={"urls": urls}, content_type="text/xml"
    )


def warmup(request):
    from weedcoco.validation import get_eppo_singleton, EPPO_CACHE_PATH

    get_eppo_singleton(EPPO_CACHE_PATH)
    return HttpResponse("Success")
