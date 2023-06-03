from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Thread)
admin.site.register(models.ChatMessage)
admin.site.register(models.ChatImageFrame)
admin.site.register(models.ChatImage)
