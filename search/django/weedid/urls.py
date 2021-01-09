from django.urls import path, re_path, include
from weedid import views

api_urlpatterns = [
    path("upload/", views.upload, name="upload"),
    path("upload_image/", views.upload_image, name="upload_image"),
    path("submit_deposit/", views.submit_deposit, name="submit_deposit"),
    path("upload_status/", views.upload_status, name="upload_status"),
    path("upload_info/", views.upload_info, name="upload_info"),
    path("upload_list/", views.upload_list, name="upload_list"),
    path("register/", views.user_register, name="user_register"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("login_status/", views.user_login_status, name="user_login_status"),
]

urlpatterns = [
    path("api/", include(api_urlpatterns)),
    re_path(r"^elasticsearch", views.elasticsearch_query, name="elasticsearch_query"),
]
