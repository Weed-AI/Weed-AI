from django.http import HttpResponse
import requests
import os
import json
from core.settings import UPLOAD_DIR, REPOSITORY_DIR
from weedid.tasks import submit_upload_task, update_index_and_thumbnails
from weedid.utils import (
    store_tmp_weedcoco,
    setup_upload_dir,
    store_tmp_image,
    create_upload_entity,
    retrieve_listing_info,
    remove_entity_local_record,
)
from weedid.models import Dataset, WeedidUser
from weedcoco.validation import validate
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseForbidden


def elasticsearch_query(request):
    elasticsearch_url = "/".join(request.path.split("/")[3:])
    elasticsearch_response = requests.post(
        url=f"http://elasticsearch:9200/{elasticsearch_url}",
        data=request.body,
        headers=request.headers,
    )
    return HttpResponse(elasticsearch_response)


def upload(request):
    if request.method == "POST":
        user_id = request.user.id
        images = []
        file_weedcoco = request.FILES["weedcoco"]
        weedcoco_json = json.load(file_weedcoco)
        validate(weedcoco_json)
        for image_reference in weedcoco_json["images"]:
            images.append(image_reference["file_name"].split("/")[-1])
        upload_dir, upload_id = setup_upload_dir(os.path.join(UPLOAD_DIR, str(user_id)))
        weedcoco_path = store_tmp_weedcoco(file_weedcoco, upload_dir)
        create_upload_entity(weedcoco_path, upload_id, user_id)
        return HttpResponse(json.dumps({"upload_id": upload_id, "images": images}))
    else:
        return HttpResponse("Only support POST request")


def upload_image(request):
    if request.method == "POST":
        user_id = request.user.id
        upload_id = request.POST["upload_id"]
        upload_image = request.FILES["upload_image"]
        upload_dir = os.path.join(UPLOAD_DIR, str(user_id), upload_id, "images")
        store_tmp_image(upload_image, upload_dir)
        return HttpResponse(f"Uploaded {upload_image.name} to {upload_dir}")
    else:
        return HttpResponse("Only support POST request")


def submit_deposit(request):
    if request.method == "POST":
        user_id = request.user.id
        upload_id = request.POST["upload_id"]
        weedcoco_path = os.path.join(
            UPLOAD_DIR, str(user_id), str(upload_id), "weedcoco.json"
        )
        images_dir = os.path.join(UPLOAD_DIR, str(user_id), str(upload_id), "images")
        submit_upload_task.delay(weedcoco_path, images_dir, upload_id)
        return HttpResponse(f"Work on user {user_id}'s upload{upload_id}")
    else:
        return HttpResponse("Only support POST request")


def upload_status(request):
    if request.user.is_authenticated:
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
    else:
        return HttpResponse("You havent been logged in")


def upload_info(request):
    if request.method == "POST":
        upload_id = request.POST["upload_id"]
        upload_entity = Dataset.objects.get(upload_id=upload_id)
        return HttpResponse(
            json.dumps(
                {
                    "metadata": upload_entity.metadata,
                    "agcontexts": upload_entity.agcontext,
                }
            )
        )
    else:
        return HttpResponse("Only support POST request")


def upload_list(request):
    upload_list = map(
        retrieve_listing_info,
        Dataset.objects.filter(status="C"),
    )
    return HttpResponse(json.dumps(list(upload_list)))


def awaiting_list(request):
    awaiting_list = map(
        retrieve_listing_info,
        Dataset.objects.filter(status="AR"),
    )
    return HttpResponse(json.dumps(list(awaiting_list)))


def dataset_approve(request, dataset_id):
    user = request.user
    if user and dataset_id and user.is_authenticated and user.is_staff:
        upload_entity = Dataset.objects.get(upload_id=dataset_id, status="AR")
        if upload_entity:
            weedcoco_path = os.path.join(
                REPOSITORY_DIR, str(dataset_id), "weedcoco.json"
            )
            update_index_and_thumbnails(weedcoco_path, dataset_id)
            return HttpResponse("It has been approved")
        else:
            return HttpResponse("Dataset to be reviewed doesnt exist")
    else:
        return HttpResponseForbidden("You dont have access to proceed")


def dataset_reject(request, dataset_id):
    user = request.user
    if user and dataset_id and user.is_authenticated and user.is_staff:
        upload_entity = Dataset.objects.get(upload_id=dataset_id, status="AR")
        if upload_entity:
            try:
                remove_entity_local_record(str(upload_entity.user_id), str(dataset_id))
            finally:
                upload_entity.status = "F"
                upload_entity.status_details = "It failed to proceed after review."
                upload_entity.save()
            return HttpResponse("The dataset has been rejected and removed")
        else:
            return HttpResponse("Dataset to be rejected doesnt exist")
    else:
        return HttpResponseForbidden("You dont have access to proceed")


def user_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = WeedidUser.objects.create_user(username, email, password)
            user.save()
            return HttpResponse("The account has been created")
        except Exception:
            return HttpResponseForbidden("You dont have access to proceed")
    else:
        return HttpResponse("Only support POST request")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = WeedidUser.objects.get(username=username)

        if user is not None and (
            user.password == password or check_password(password, user.password)
        ):
            login(request, user)
            return HttpResponse("You have been logged in")
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponse("Only support POST request")


def user_logout(request):
    logout(request)
    return HttpResponse("You have been logged out")


def user_login_status(request):
    if request.user.is_authenticated:
        return HttpResponse("You have been logged in")
    else:
        return HttpResponseForbidden("You havent been logged in")


def login_google(request):
    if request.method == "POST":
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
    else:
        return HttpResponse("Only support POST request")
