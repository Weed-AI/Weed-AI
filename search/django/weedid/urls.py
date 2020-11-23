from django.urls import path, re_path
from weedid import views

urlpatterns = [
    path("api/test/", views.test, name="test"),
    path("api/upload/", views.upload, name="upload"),
    path("api/upload_image/", views.upload_image, name="upload_image"),
    path("api/submit_deposit/", views.submit_deposit, name="submit_deposit"),
    re_path(r"^elasticsearch", views.elasticsearch_query, name="elasticsearch_query"),
]
