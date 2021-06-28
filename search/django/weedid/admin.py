# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import WeedidUser, Dataset
from .tasks import reindex_dataset, redeposit_dataset


@admin.action(
    description="Reindex this content in Elastic Search and regenerate thumbnails"
)
def reindex(modeladmin, request, datasets):
    for dataset in datasets:
        reindex_dataset.delay(dataset.upload_id)


@admin.action(
    description="Recreate repository and download entry using metadata and agcontexts from database, as well as updated algorithms"
)
def redeposit(modeladmin, request, datasets):
    for dataset in datasets:
        redeposit_dataset.delay(dataset.upload_id)


reindex.short_description = "Re-index selected datasets"
redeposit.short_description = "Re-deposit selected datasets"


class DatasetAdmin(admin.ModelAdmin):

    list_display = ["upload_id", "name", "status", "date"]
    search_fields = ["status"]
    ordering = ["status", "date"]
    actions = [reindex, redeposit]

    def name(self, instance):
        return (instance.metadata or {}).get("name", "<Untitled>")


admin.site.register(WeedidUser)
admin.site.register(Dataset, DatasetAdmin)
