from django.contrib import admin
from . import models

admin.site.register(models.GeoJsonFile)
admin.site.register(models.Chunk)
