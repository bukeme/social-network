from django.contrib import admin
from groups import models

# Register your models here.

admin.site.register(models.CustomGroup)
admin.site.register(models.GroupProfileImage)
