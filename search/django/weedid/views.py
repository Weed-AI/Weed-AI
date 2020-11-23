from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import os
import json
from core.settings import UPLOAD_DIR
from weedid.tasks import upload_task
from weedid.utils import store_tmp_weedcoco, setup_upload_dir, store_tmp_image


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
        user_id = 1
        images = []
        file_weedcoco = request.FILES["weedcoco"]
        for image_reference in json.load(file_weedcoco)["images"]:
            images.append(image_reference["file_name"].split("/")[-1])
        upload_dir, upload_id = setup_upload_dir(os.path.join(UPLOAD_DIR, str(user_id)))
        store_tmp_weedcoco(file_weedcoco, upload_dir)
        return HttpResponse(json.dumps({"upload_id": upload_id, "images": images}))


@csrf_exempt
def upload_image(request):
    if request.method == "GET":
        return HttpResponse("Only support POST request")
    elif request.method == "POST":
        user_id = 1
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
        user_id = 1
        upload_id = request.POST["upload_id"]
        weedcoco_path = os.path.join(
            UPLOAD_DIR, str(user_id), str(upload_id), "weedcoco.json"
        )
        images_dir = os.path.join(UPLOAD_DIR, str(user_id), str(upload_id), "images")
        upload_task.delay(weedcoco_path, images_dir)
        return HttpResponse(f"Work on user {user_id}'s upload{upload_id}")
