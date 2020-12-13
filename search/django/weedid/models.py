from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser


class Dataset(models.Model):
    UPLOAD_STATUS_CHOICES = [
        ("N", "None"),
        ("P", "Processing"),
        ("I", "Incomplete"),
        ("AR", "Awaiting Review"),
        ("F", "Failed"),
        ("C", "Complete"),
    ]
    metadata = JSONField(null=True)
    upload_id = models.CharField(
        primary_key=True, max_length=20, null=False, blank=False, unique=True
    )
    upload_agcontext = JSONField(null=True)
    upload_date = models.DateField(auto_now_add=True, blank=True, null=True)
    upload_user = models.ForeignKey(
        "WeedidUser",
        related_name="user",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    upload_status = models.CharField(
        max_length=2, choices=UPLOAD_STATUS_CHOICES, default="N"
    )
    upload_status_details = models.CharField(
        max_length=50, null=True, blank=True, default=""
    )
    upload_annotation_type = models.CharField(max_length=20, default="WeedCOCO")


class WeedidUser(AbstractUser):
    latest_upload = models.ForeignKey(
        Dataset, related_name="upload", on_delete=models.SET_NULL, blank=True, null=True
    )
    accessible_datasets = models.ManyToManyField(
        Dataset, related_name="accessible_dataset", blank=True
    )
