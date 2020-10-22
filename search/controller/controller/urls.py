from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from weedid import urls as weedid_urls

urlpatterns = [
    path(
        "controller/",
        include([path("admin/", admin.site.urls), path("", include(weedid_urls))]),
    )
]
