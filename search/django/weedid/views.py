from django.http import HttpResponse
import requests
import os
import json
from core.settings import UPLOAD_DIR
from weedid.tasks import submit_upload_task
from weedid.utils import (
    store_tmp_weedcoco,
    setup_upload_dir,
    store_tmp_image,
    create_upload_entity,
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
    if request.method == "POST":
        user = request.user
        if user and user.is_authenticated:
            try:
                images = []
                file_weedcoco = request.FILES["weedcoco"]
                weedcoco_json = json.load(file_weedcoco)
                # initially use more lenient validation.
                validate(weedcoco_json, schema="compatible-coco")
                for image_reference in weedcoco_json["images"]:
                    images.append(image_reference["file_name"].split("/")[-1])
                upload_dir, upload_id = setup_upload_dir(
                    os.path.join(UPLOAD_DIR, str(user.id))
                )
                weedcoco_path = store_tmp_weedcoco(file_weedcoco, upload_dir)
                create_upload_entity(weedcoco_path, upload_id, user.id)
            except ValidationError as e:
                return HttpResponseForbidden(str(e))
            except Exception:
                return HttpResponseForbidden("There is something wrong with the file")
            else:
                return HttpResponse(
                    json.dumps({"upload_id": upload_id, "images": images})
                )
        else:
            return HttpResponseForbidden("You dont have access to proceed")
    else:
        return HttpResponseNotAllowed(request.method)


def upload_image(request):
    if request.method == "POST":
        user = request.user
        if user and user.is_authenticated:
            upload_id = request.POST["upload_id"]
            upload_image = request.FILES["upload_image"]
            upload_dir = os.path.join(UPLOAD_DIR, str(user.id), upload_id, "images")
            store_tmp_image(upload_image, upload_dir)
            return HttpResponse(f"Uploaded {upload_image.name} to {upload_dir}")
        else:
            return HttpResponseForbidden("You dont have access to proceed")
    else:
        return HttpResponseNotAllowed(request.method)


def upload_agcontexts(request):
    if request.method == "POST":
        user = request.user
        if user and user.is_authenticated:
            data = json.loads(request.body)
            upload_id, ag_contexts = data["upload_id"], data["ag_contexts"]
            weedcoco_path = os.path.join(
                UPLOAD_DIR, str(user.id), str(upload_id), "weedcoco.json"
            )
            try:
                add_agcontexts(weedcoco_path, ag_contexts)
                Dataset.objects.filter(upload_id=upload_id).update(
                    agcontext=[ag_contexts]
                )
            except Exception:
                return HttpResponseNotAllowed("Failed to add AgContexts")
            else:
                return HttpResponse(
                    f"Updated AgContexts for user {user.id}'s upload{upload_id}"
                )
        else:
            return HttpResponseForbidden("You dont have access to proceed")
    else:
        return HttpResponseNotAllowed(request.method)


def submit_deposit(request):
    if request.method == "POST":
        user = request.user
        if user and user.is_authenticated:
            upload_id = request.POST["upload_id"]
            weedcoco_path = os.path.join(
                UPLOAD_DIR, str(user.id), str(upload_id), "weedcoco.json"
            )
            images_dir = os.path.join(
                UPLOAD_DIR, str(user.id), str(upload_id), "images"
            )
            submit_upload_task.delay(weedcoco_path, images_dir, upload_id)
            return HttpResponse(f"Work on user {user.id}'s upload{upload_id}")
        else:
            return HttpResponseForbidden("You dont have access to proceed")
    else:
        return HttpResponseNotAllowed(request.method)


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
        return HttpResponseNotAllowed(request.method)


def upload_list(request):
    upload_list = map(
        lambda queryEntity: {
            "name": queryEntity.metadata["info"][0]["name"]
            if "name" in queryEntity.metadata["info"][0]
            else "",
            "upload_id": queryEntity.upload_id,
            "upload_date": str(queryEntity.date),
            "contributor": queryEntity.user.username,
        },
        Dataset.objects.filter(status="C"),
    )
    return HttpResponse(json.dumps(list(upload_list)))


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
            return HttpResponseForbidden()
    else:
        return HttpResponseNotAllowed(request.method)


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
        return HttpResponseNotAllowed(request.method)


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
        return HttpResponseNotAllowed(request.method)
