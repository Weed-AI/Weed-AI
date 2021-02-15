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
    add_agcontexts,
)
from weedid.models import Dataset, WeedidUser
from weedcoco.validation import validate, ValidationError
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseForbidden, HttpResponseNotAllowed


def elasticsearch_query(request):
    elasticsearch_url = "/".join(request.path.split("/")[3:])
    elasticsearch_response = requests.post(
        url=f"http://elasticsearch:9200/{elasticsearch_url}",
        data=request.body,
        headers=request.headers,
    )
    return HttpResponse(elasticsearch_response)


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
        validate(weedcoco_json)
        for image_reference in weedcoco_json["images"]:
            images.append(image_reference["file_name"].split("/")[-1])
        upload_dir, upload_id = setup_upload_dir(os.path.join(UPLOAD_DIR, str(user.id)))
        weedcoco_path = store_tmp_weedcoco(file_weedcoco, upload_dir)
        create_upload_entity(weedcoco_path, upload_id, user.id)
    except ValidationError as e:
        return HttpResponseForbidden(str(e))
    except Exception:
        return HttpResponseForbidden("There is something wrong with the file")
    else:
        return HttpResponse(json.dumps({"upload_id": upload_id, "images": images}))


def upload_image(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(request.method)
    user = request.user
    if not (user and user.is_authenticated):
        return HttpResponseForbidden("You dont have access to proceed")
    upload_id = request.POST["upload_id"]
    upload_image = request.FILES["upload_image"]
    upload_dir = os.path.join(UPLOAD_DIR, str(user.id), upload_id, "images")
    store_tmp_image(upload_image, upload_dir)
    return HttpResponse(f"Uploaded {upload_image.name} to {upload_dir}")


def upload_agcontexts(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(request.method)
    user = request.user
    if not (user and user.is_authenticated):
        return HttpResponseForbidden("You dont have access to proceed")
    data = json.loads(request.body)
    upload_id, ag_contexts = data["upload_id"], data["ag_contexts"]
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


def upload_info(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(request.method)
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


def upload_list(request):
    upload_list = map(
        retrieve_listing_info,
        Dataset.objects.filter(status="C"),
    )
    return HttpResponse(json.dumps(list(upload_list)))


def awaiting_list(request):
    user = request.user
    if not (user and user.is_authenticated and user.is_staff):
        return HttpResponseForbidden("You dont have access to proceed")
    awaiting_list = map(
        retrieve_listing_info,
        Dataset.objects.filter(status="AR"),
    )
    return HttpResponse(json.dumps(list(awaiting_list)))


def dataset_approve(request, dataset_id):
    user = request.user
    if not (user and dataset_id and user.is_authenticated and user.is_staff):
        return HttpResponseForbidden("You dont have access to proceed")
    upload_entity = Dataset.objects.get(upload_id=dataset_id, status="AR")
    if upload_entity:
        weedcoco_path = os.path.join(REPOSITORY_DIR, str(dataset_id), "weedcoco.json")
        update_index_and_thumbnails(weedcoco_path, dataset_id)
        return HttpResponse("It has been approved")
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
        return HttpResponse("The dataset has been rejected and removed")
    else:
        return HttpResponseNotAllowed("Dataset to be rejected doesn't exist")


def user_register(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(request.method)
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    try:
        user = WeedidUser.objects.create_user(username, email, password)
        user.save()
        return HttpResponse("The account has been created")
    except Exception:
        return HttpResponseForbidden("You dont have access to proceed")


def user_login(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(request.method)
    username = request.POST["username"]
    password = request.POST["password"]
    user = WeedidUser.objects.get(username=username)

    if user is not None and (
        user.password == password or check_password(password, user.password)
    ):
        login(request, user)
        return HttpResponse("You have been logged in")
    else:
        return HttpResponseForbidden("Wrong login credentials")


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
