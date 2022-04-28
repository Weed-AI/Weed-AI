from djproxy.views import HttpProxy
import re

from core.settings import TUS_SERVER


class ProxyRelativeLocation(object):
    def process_response(self, proxy, request, upstream_response, response):
        if response.has_header("Location"):
            response["Location"] = re.sub("^https?://[^/]+", "", response["Location"])
        return response


class TusProxy(HttpProxy):
    base_url = TUS_SERVER
    proxy_middleware = [
        "djproxy.proxy_middleware.AddXFF",
        "djproxy.proxy_middleware.AddXFH",
        "djproxy.proxy_middleware.AddXFP",
        "djproxy.proxy_middleware.ProxyPassReverse",
        "weedid.tus.ProxyRelativeLocation",
    ]
