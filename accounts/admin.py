from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.ProfileImage)
admin.site.register(models.CoverImage)
admin.site.register(models.FriendRequest)
