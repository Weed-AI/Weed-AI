from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser


class Dataset(models.Model):
    upload_id = models.CharField(
        primary_key=True, max_length=40, null=False, blank=False, unique=True
    )
    STATUS_CHOICES = [
        ("N", "None"),
        ("P", "Processing"),
        ("I", "Incomplete"),
        ("AR", "Awaiting Review"),
        ("F", "Failed"),
        ("C", "Complete"),
    ]
    metadata = JSONField(null=True)
    agcontext = JSONField(null=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey(
        "WeedidUser",
        related_name="user",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="N")
    status_details = models.TextField(null=True, blank=True)
    annotation_format = models.CharField(max_length=20, default="WeedCOCO")
    head_version = models.PositiveIntegerField(default=1)


class WeedidUser(AbstractUser):
    latest_upload = models.ForeignKey(
        Dataset, related_name="upload", on_delete=models.SET_NULL, blank=True, null=True
    )
