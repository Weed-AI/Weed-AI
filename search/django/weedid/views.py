from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import os
import json
from core.settings import UPLOAD_DIR
from weedid.tasks import upload_task
from weedid.utils import (
    store_tmp_weedcoco,
    setup_upload_dir,
    store_tmp_image,
    create_upload_entity,
)
from weedid.models import Dataset, WeedidUser
import time


def test(request):
    return HttpResponse("TESTING VIEW")


@csrf_exempt
def elasticsearch_query(request):
    elasticsearch_url = "/".join(request.path.split("/")[3:])
    elasticsearch_response = requests.post(
        url=f"http://elasticsearch:9200/{elasticsearch_url}",
        data=request.body,
        headers=request.headers,
    )
    return HttpResponse(elasticsearch_response)


@csrf_exempt
def upload(request):
    if request.method == "GET":
        return HttpResponse("Only support POST request")
    elif request.method == "POST":
        user_id = 2
        images = []
        file_weedcoco = request.FILES["weedcoco"]
        for image_reference in json.load(file_weedcoco)["images"]:
            images.append(image_reference["file_name"].split("/")[-1])
        upload_dir, upload_id = setup_upload_dir(os.path.join(UPLOAD_DIR, str(user_id)))
        weedcoco_path = store_tmp_weedcoco(file_weedcoco, upload_dir)
        create_upload_entity(weedcoco_path, upload_id, user_id)
        return HttpResponse(json.dumps({"upload_id": upload_id, "images": images}))


@csrf_exempt
def upload_image(request):
    if request.method == "GET":
        return HttpResponse("Only support POST request")
    elif request.method == "POST":
        time.sleep(3)
        user_id = 2
        upload_id = request.POST["upload_id"]
        upload_image = request.FILES["upload_image"]
        upload_dir = os.path.join(UPLOAD_DIR, str(user_id), upload_id, "images")
        store_tmp_image(upload_image, upload_dir)
        return HttpResponse(f"Uploaded {upload_image.name} to {upload_dir}")


@csrf_exempt
def submit_deposit(request):
    if request.method == "GET":
        return HttpResponse("Only support POST request")
    elif request.method == "POST":
        user_id = 2
        upload_id = request.POST["upload_id"]
        weedcoco_path = os.path.join(
            UPLOAD_DIR, str(user_id), str(upload_id), "weedcoco.json"
        )
        images_dir = os.path.join(UPLOAD_DIR, str(user_id), str(upload_id), "images")
        upload_task.delay(weedcoco_path, images_dir, upload_id)
        return HttpResponse(f"Work on user {user_id}'s upload{upload_id}")


def upload_status(request):
    user_id = 2
    upload_entity = WeedidUser.objects.get(id=user_id).latest_upload
    return HttpResponse(
        json.dumps(
            {
                "upload_status": upload_entity.upload_status,
                "upload_status_details": upload_entity.upload_status_details,
            }
        )
    )


@csrf_exempt
def upload_info(request):
    if request.method == "GET":
        return HttpResponse("Only support POST request")
    elif request.method == "POST":
        upload_id = request.POST["upload_id"]
        upload_entity = Dataset.objects.get(upload_id=upload_id)
        return HttpResponse(
            json.dumps(
                {
                    "metadata": upload_entity.metadata,
                    "agcontexts": upload_entity.upload_agcontext,
                }
            )
        )


def upload_list(request):
    upload_list = map(
        lambda queryEntity: {
            "name": queryEntity.metadata["info"][0]["name"]
            if "name" in queryEntity.metadata["info"][0]
            else "",
            "upload_id": queryEntity.upload_id,
            "upload_date": str(queryEntity.upload_date),
            "contributor": queryEntity.upload_user.username,
        },
        Dataset.objects.filter(upload_status="C"),
    )
    return HttpResponse(json.dumps(list(upload_list)))
