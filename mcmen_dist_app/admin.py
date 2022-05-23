from django.contrib import admin
from . import models
admin.site.site_header = "McMenamins Distribution"

admin.site.register(models.Driver)
admin.site.register(models.Property)
admin.site.register(models.Route)
admin.site.register(models.Article)
admin.site.register(models.PostComment)
admin.site.register(models.Images)