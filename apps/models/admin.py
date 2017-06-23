from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from . import models

admin.site.register(models.Node, LeafletGeoAdmin)
admin.site.register(models.Reuse, LeafletGeoAdmin)
admin.site.register(models.Post)
admin.site.register(models.Agreement)
admin.site.register(models.Reference)
admin.site.register(models.Material)
admin.site.register(models.Sms)
