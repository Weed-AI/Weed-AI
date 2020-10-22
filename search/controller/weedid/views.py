from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests


def test(request):
    return HttpResponse("TESTING VIEW")


@csrf_exempt
def elasticsearchQuery(request):
    elasticsearch_url = "/".join(request.path.split("/")[3:])
    elasticsearch_response = requests.post(
        url=f"http://elasticsearch:9200/{elasticsearch_url}",
        data=request.body,
        headers=request.headers,
    )
    return HttpResponse(elasticsearch_response)
