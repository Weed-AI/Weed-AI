from django.urls import path, re_path, include
from django_tus.views import TusUpload
from weedid import views

api_urlpatterns = [
    path("upload/", views.upload, name="upload"),
    path("warmup/", views.warmup, name="warmup"),
    path("upload_voc/", views.VocUploader.upload, name="upload_voc"),
    path("remove_voc/", views.VocUploader.remove, name="remove_voc"),
    path("submit_voc/", views.VocUploader.submit, name="submit_voc"),
    path("move_voc/", views.VocUploader.move, name="move_voc"),
    path("upload_mask/", views.MaskUploader.upload, name="upload_mask"),
    path("remove_mask/", views.MaskUploader.remove, name="remove_mask"),
    path("submit_mask/", views.MaskUploader.submit, name="submit_mask"),
    path("move_mask/", views.MaskUploader.move, name="move_mask"),
    path("upload_image/", views.upload_image, name="upload_image"),
    path("upload_image_zip/", views.upload_image_zip, name="upload_image_zip"),
    path("update_categories/", views.update_categories, name="update_categories"),
    path("upload_agcontexts/", views.upload_agcontexts, name="upload_agcontexts"),
    path("upload_metadata/", views.upload_metadata, name="upload_metadata"),
    path("upload_tus/", TusUpload.as_view(), name="tus_upload"),
    path("upload_tus/<uuid:resource_id>", TusUpload.as_view(), name="ts_upload_chunks"),
    path("submit_deposit/", views.submit_deposit, name="submit_deposit"),
    path("upload_status/", views.upload_status, name="upload_status"),
    path("upload_info/<str:dataset_id>", views.upload_info, name="upload_info"),
    path("upload_list/", views.upload_list, name="upload_list"),
    path("awaiting_list/", views.awaiting_list, name="awaiting_list"),
    path(
        "dataset_approve/<str:dataset_id>",
        views.dataset_approve,
        name="dataset_approve",
    ),
    path(
        "dataset_reject/<str:dataset_id>", views.dataset_reject, name="dataset_reject"
    ),
    path("register/", views.user_register, name="user_register"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("login_status/", views.user_login_status, name="user_login_status"),
    path("login_google/", views.login_google, name="login_google"),
    path("set_csrf/", views.set_csrf),
]

urlpatterns = [
    path("api/", include(api_urlpatterns)),
    re_path(r"^elasticsearch", views.elasticsearch_query, name="elasticsearch_query"),
    path("sitemap.xml", views.sitemap_xml),
]
