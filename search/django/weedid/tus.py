from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
import logging
import traceback
import requests

from core.settings import TUS_HOST

from djproxy.headers import HeaderDict

logger = logging.getLogger()

# Note - getting this working is hitting many HTTP niggles, to the extent that
# I think the solution wouldn't be very maintainable.


def upload_tus(request, resource_id=None):
    """Reverse proxy to tusd with authentication"""
    user = request.user
    logger.warn(f"in upload_tus {resource_id}")
    if not (user and user.is_authenticated):
        logger.error("User is not authenticated")
        return HttpResponseForbidden("You dont have access to proceed")
    try:
        headers = HeaderDict.from_request(request)
        logger.warn(f"demunged request headers = {headers}")
        # X-Forwarded-Host is set at the nginx reverse proxy
        headers["Host"] = headers["X-Forwarded-Host"]
        method = request.method
        data = request.body
        tus_url = TUS_HOST + "tus/files"
        if resource_id:
            tus_url += "/" + resource_id
        logger.warn(f"sending to tus {method} {tus_url} {headers}")
        tus_response = requests.request(method, tus_url, data=data, headers=headers)
        logger.warn(f"tus response {tus_response} {tus_response.status_code}")
        django_response = HttpResponse(
            content=tus_response.content, status=tus_response.status_code
        )
        for k, v in tus_response.headers.items():
            django_response[k] = v
        logger.warn(f"Returning {django_response}, {django_response.items()}")
        return django_response
    except Exception as e:
        traceback.print_exc()
        return HttpResponseBadRequest(str(e))
