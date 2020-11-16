from django.urls import path, re_path
from weedid import views

urlpatterns = [
    path("api/", views.test, name="test"),
    re_path(r"^elasticsearch", views.elasticsearch_query, name="elasticsearch_query"),
]
