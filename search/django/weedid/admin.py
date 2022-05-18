# from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Dataset, WeedidUser
from .tasks import redeposit_dataset, reindex_dataset, remove_dataset


def reindex(modeladmin, request, datasets):
    for dataset in datasets:
        reindex_dataset.delay(dataset.upload_id)


def redeposit(modeladmin, request, datasets):
    for dataset in datasets:
        redeposit_dataset.delay(dataset.upload_id)


def remove(modeladmin, request, datasets):
    for dataset in datasets:
        remove_dataset.delay(dataset.upload_id)


reindex.short_description = (
    "Reindex this content in Elastic Search and regenerate thumbnails"
)
redeposit.short_description = "Recreate repository and download entry using metadata and agcontexts from database, as well as updated algorithms"
remove.short_description = "Remove repository and upload record, dataset entity, zipfile and index of a dataset"


class DatasetAdmin(admin.ModelAdmin):

    list_display = ["upload_id", "name", "status", "date"]
    search_fields = ["status"]
    ordering = ["status", "date"]
    actions = [reindex, redeposit, remove]

    def name(self, instance):
        return (instance.metadata or {}).get("name", "<Untitled>")


admin.site.register(WeedidUser)
admin.site.register(Dataset, DatasetAdmin)
