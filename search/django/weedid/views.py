import json
import logging
import os
import shutil
import traceback
from pathlib import Path
from zipfile import ZipFile

import requests
from core.settings import (
    CVAT_DATA_DIR,
    IMAGE_HASH_MAPPING_URL,
    MAX_IMAGE_SIZE,
    MAX_VOC_SIZE,
    REPOSITORY_DIR,
    SITE_BASE_URL,
    TUS_DESTINATION_DIR,
    UPLOAD_DIR,
)
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.exceptions import PermissionDenied
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    HttpResponseServerError,
)
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from weedcoco.importers.mask import generate_paths_from_mask_only, masks_to_coco
from weedcoco.importers.voc import voc_to_coco
from weedcoco.importers.yolo import yolo_to_coco
from weedcoco.repo.deposit import Repository, mkdir_safely
from weedcoco.utils import fix_compatibility_quirks
from weedcoco.validation import JsonValidationError, validate, validate_json

from weedid.decorators import check_post_and_authenticated
from weedid.models import Dataset, WeedidUser
from weedid.notification import review_notification
from weedid.tasks import (
    store_tmp_image_from_zip,
    submit_upload_task,
    update_index_and_thumbnails,
)
from weedid.utils import (
    add_agcontexts,
    add_metadata,
    create_upload_entity,
    move_to_upload,
    parse_category_for_mapper,
    remove_entity_local_record,
    retrieve_listing_info,
    retrieve_missing_images_list,
    set_categories,
    setup_upload_dir,
    store_tmp_image,
    store_tmp_voc,
    store_tmp_weedcoco,
    upload_helper,
    validate_email_format,
)

logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def set_csrf(request):
    return HttpResponse("Success")


def json_validation_response(exc):
    return HttpResponseBadRequest(
        json.dumps(exc.get_error_details()), content_type="application/json"
    )


def check_ownership(upload_id, user_id, message="Permission Denied"):
    dataset = Dataset.objects.get(upload_id=upload_id)
    if dataset.user.id != user_id:
        raise PermissionDenied(message)


@require_http_methods(["GET", "POST"])
def elasticsearch_query(request):
    try:
        elasticsearch_url = "/".join(request.path.split("/")[2:])
    except Exception:
        return HttpResponseBadRequest("Invalid query format")
    if not elasticsearch_url.startswith("weedid/_msearch"):
        return HttpResponseBadRequest("Only _msearch queries are currently forwarded")
    elasticsearch_response = requests.post(
        url=f"http://elasticsearch:9200/{elasticsearch_url}",
        data=request.body,
        headers=request.headers,
    )
    return HttpResponse(elasticsearch_response)


@require_http_methods(["POST"])
@login_required
def upload(request):
    user = request.user
    try:
        images = []
        file_weedcoco = request.FILES["weedcoco"]
        weedcoco_json = json.load(file_weedcoco)
        fix_compatibility_quirks(weedcoco_json)
        if request.POST["upload_mode"] == "edit":
            upload_id, images, categories = upload_helper(
                weedcoco_json,
                user.id,
                request.POST["schema"],
                request.POST["upload_id"],
            )
            if len(images) == len(weedcoco_json["images"]):
                logger.error("All weedcoco files missing in edited dataset")
                return HttpResponseBadRequest(
                    "weedcoco.json does not match earlier version"
                )
        else:
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


def retrieve_cvat_task(request, upload_id, task_id):
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
                upload_id, images, categories = upload_helper(
                    coco_json, user.id, upload_id=upload_id
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
                {
                    "upload_id": upload_id,
                    "images": images,
                    "categories": categories,
                }
            )
        )


def editing_init(request, dataset_id):
    user = request.user
    if not (user and user.is_authenticated):
        return HttpResponseForbidden("You dont have access to proceed")
    upload_entity = Dataset.objects.get(upload_id=dataset_id, status="C")
    if upload_entity.user.id != user.id:
        return HttpResponseForbidden("You dont have access to edit")
    upload_path = os.path.join(UPLOAD_DIR, str(user.id), dataset_id)
    repository = Repository(REPOSITORY_DIR)
    dataset = repository.dataset(dataset_id)
    dataset.extract_original_images(
        upload_path, redis_mapping_url=IMAGE_HASH_MAPPING_URL
    )

    with open(os.path.join(upload_path, "weedcoco.json")) as f:
        weedcoco_json = json.load(f)
        categories = [
            parse_category_for_mapper(category)
            for category in weedcoco_json["categories"]
        ]
        images = retrieve_missing_images_list(
            weedcoco_json, os.path.join(upload_path, "images"), dataset_id
        )
    return HttpResponse(
        json.dumps(
            {
                "upload_id": dataset_id,
                "agcontext": upload_entity.agcontext,
                "metadata": upload_entity.metadata,
                "categories": categories,
                "images": images,
            }
        )
    )


class CustomUploader:
    @classmethod
    @check_post_and_authenticated
    def upload(cls, request):
        user = request.user
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
    @check_post_and_authenticated
    def remove(cls, request):
        user = request.user
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
    @check_post_and_authenticated
    def move(cls, request):
        user = request.user
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
    @check_post_and_authenticated
    def submit(cls, request):
        user = request.user
        try:
            store_id = request.POST[cls.id_name]
            if "/" in store_id:
                return HttpResponseBadRequest("Bad id")
            coco_json = cls.convert_to_coco(
                Path(os.path.join(UPLOAD_DIR, str(user.id), store_id)), request
            )
            validate(coco_json, schema="coco")
            fix_compatibility_quirks(coco_json)
            categories = [
                parse_category_for_mapper(category)
                for category in coco_json["categories"]
            ]
            upload_dir, upload_id = setup_upload_dir(
                os.path.join(UPLOAD_DIR, str(user.id))
            )
            images = retrieve_missing_images_list(
                coco_json, os.path.join(upload_dir, "images"), upload_id
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


class YoloUploader(CustomUploader):
    mode = "yolo"
    id_name = "yolo_id"
    payload_name = "yolo_file"
    remove_name = "yolo_filename"
    max_file_size = MAX_VOC_SIZE
    store_tmp = store_tmp_voc

    @classmethod
    @check_post_and_authenticated
    def submit(cls, request):
        user = request.user
        try:
            store_id = request.POST[cls.id_name]
            upload_id = request.POST["upload_id"]  # Get the existing upload_id
            if "/" in store_id or "/" in upload_id:
                return HttpResponseBadRequest("Bad id")

            store_dir = Path(UPLOAD_DIR) / str(user.id) / store_id

            upload_dir = Path(UPLOAD_DIR) / str(user.id) / upload_id

            coco_json = cls.convert_to_coco(store_dir, request)

            validate(coco_json, schema="compatible-coco")
            fix_compatibility_quirks(coco_json)

            categories = [
                parse_category_for_mapper(category)
                for category in coco_json["categories"]
            ]

            images = retrieve_missing_images_list(
                coco_json, upload_dir / "images", upload_id
            )

            store_tmp_weedcoco(coco_json, str(upload_dir))

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

    @staticmethod
    def convert_to_coco(store_path, request):
        user = request.user
        upload_id = request.POST["upload_id"]
        image_dir = Path(UPLOAD_DIR) / str(user.id) / upload_id / "images"

        if not image_dir.is_dir():
            raise FileNotFoundError("Image directory not found. Please upload images before submitting annotations.")

        return yolo_to_coco(store_path, image_dir)

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


@login_required
@require_http_methods(["POST"])
def upload_image(request):
    user = request.user
    upload_id = request.POST["upload_id"]
    check_ownership(upload_id, user.id, "No permission to upload")
    upload_image = request.FILES["upload_image"]
    if upload_image.size > MAX_IMAGE_SIZE:
        return HttpResponseBadRequest("This image has exceeded the size limit!")
    upload_dir = os.path.join(UPLOAD_DIR, str(user.id), upload_id, "images")
    store_tmp_image(upload_image, upload_dir)
    return HttpResponse(f"Uploaded {upload_image.name} to {upload_dir}")


@login_required
@require_http_methods(["POST"])
def unpack_image_zip(request):
    """Unpack a zipfile which has been uploaded via tus"""
    user = request.user
    upload_id = request.POST["upload_id"]
    upload_image_zip = request.POST["upload_image_zip"]
    # Get list of missing images from frontend to calculate images that are still missing after the current zip being uploaded
    images = request.POST["images"].split(",")
    zipfile = os.path.join(TUS_DESTINATION_DIR, upload_image_zip)
    upload_dir = os.path.join(UPLOAD_DIR, str(user.id), upload_id, "images")
    celery_task = store_tmp_image_from_zip.delay(upload_id, zipfile, upload_dir, images)
    return HttpResponse(json.dumps({"task_id": celery_task.id}))


def check_image_zip(request, task_id):
    result = store_tmp_image_from_zip.AsyncResult(task_id)
    if not result.ready():
        return HttpResponse("wait", status_code=202)
    return HttpResponse(json.dumps(result.get(propagate=True)))


@login_required
@require_http_methods(["POST"])
def update_categories(request):
    user = request.user
    data = json.loads(request.body)
    upload_id, categories = data["upload_id"], data["categories"]
    check_ownership(upload_id, user.id, "No permission to update")
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


@login_required
@require_http_methods(["POST"])
def upload_agcontexts(request):
    user = request.user
    data = json.loads(request.body)
    upload_id, ag_contexts = data["upload_id"], data["ag_contexts"]
    check_ownership(upload_id, user.id, "No permission to update")
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


@login_required
@require_http_methods(["POST"])
def upload_metadata(request):
    user = request.user
    data = json.loads(request.body)
    upload_id, metadata = data["upload_id"], data["metadata"]
    check_ownership(upload_id, user.id, "No permission to update")
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
        return HttpResponse(f"Updated Metadata for user {user.id}'s upload{upload_id}")


@login_required
@require_http_methods(["POST"])
def copy_cvat(request):
    """Copy the images for a CVAT task from the CVAT volume to the upload dir"""
    user = request.user
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


@login_required
@require_http_methods(["POST"])
def submit_deposit(request):
    user = request.user
    upload_id = request.POST["upload_id"]
    check_ownership(upload_id, user.id, "No permission to submit")
    weedcoco_path = os.path.join(
        UPLOAD_DIR, str(user.id), str(upload_id), "weedcoco.json"
    )
    images_dir = os.path.join(UPLOAD_DIR, str(user.id), str(upload_id), "images")
    submit_upload_task.delay(
        weedcoco_path,
        images_dir,
        upload_id,
        mode=request.POST["upload_mode"],
    )
    return HttpResponse(f"Work on user {user.id}'s upload{upload_id}")


@login_required
def upload_status(request):
    user_id = request.user.id
    upload_entity = WeedidUser.objects.get(id=user_id).latest_upload

    if upload_entity is not None:
        status = upload_entity.status
        details = upload_entity.status_details
    else:
        status = "N"
        details = ""

    return HttpResponse(
        json.dumps(
            {
                "upload_status": status,
                "upload_status_details": details,
            }
        )
    )


@require_http_methods(["GET"])
def upload_info(request, dataset_id):
    upload_entity = Dataset.objects.get(upload_id=dataset_id)
    return HttpResponse(
        json.dumps(
            {
                "metadata": upload_entity.metadata,
                "agcontexts": upload_entity.agcontext,
                "head_version": upload_entity.head_version,
            }
        )
    )


def upload_list(request):
    user_id = request.user.id if request.user else 0
    upload_list = [
        retrieve_listing_info(dataset, awaiting_review=False, user_id=user_id)
        for dataset in Dataset.objects.filter(status="C")
    ]
    return HttpResponse(json.dumps(upload_list))


@login_required
@staff_member_required
def awaiting_list(request):
    awaiting_list = [
        retrieve_listing_info(dataset, awaiting_review=True)
        for dataset in Dataset.objects.filter(status="AR")
    ]
    return HttpResponse(json.dumps(awaiting_list))


@login_required
@staff_member_required
def dataset_approve(request, dataset_id):
    upload_entity = Dataset.objects.get(upload_id=dataset_id, status="AR")
    if upload_entity:
        update_index_and_thumbnails.delay(dataset_id)
        upload_entity.status = "P"
        upload_entity.status_details = "It's now being indexed"
        upload_entity.save()
        return HttpResponse("It has been sent to be indexed")
    else:
        return HttpResponseNotAllowed("Dataset to be reviewed doesn't exist")


@login_required
@staff_member_required
def dataset_reject(request, dataset_id):
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


@require_http_methods(["POST"])
def user_register(request):
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


@require_http_methods(["POST"])
def user_login(request):
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


@require_http_methods(["POST"])
def login_google(request):
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
