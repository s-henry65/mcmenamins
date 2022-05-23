from django.contrib import admin
from . import models

admin.site.register(models.Brewer)
admin.site.register(models.Brewery)
admin.site.register(models.Kegs)
