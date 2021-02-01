# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import WeedidUser, Dataset

admin.site.register(WeedidUser)
admin.site.register(Dataset)
