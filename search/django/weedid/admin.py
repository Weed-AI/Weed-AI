# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import WeedidUser, Dataset
from .tasks import reindex_dataset


def reindex(modeladmin, request, datasets):
    for dataset in datasets:
        reindex_dataset.delay(dataset.upload_id)


reindex.short_description = "Re-index selected datasets"


class DatasetAdmin(admin.ModelAdmin):

    list_display = ["upload_id", "name", "status", "date"]
    ordering = ["status", "date"]
    actions = [reindex]

    def name(self, instance):
        return instance.metadata["name"]


admin.site.register(WeedidUser)
admin.site.register(Dataset, DatasetAdmin)
