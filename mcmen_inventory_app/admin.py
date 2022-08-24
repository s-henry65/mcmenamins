from django.contrib import admin
from . import models


# admin.site.register(models.Brewer)
admin.site.register(models.Brewery)
admin.site.register(models.Kegs)


# class InventoryAdmin(admin.ModelAdmin):
#     list_display = ('beer', 'brewery', 'quantity')

# admin.site.register(InventoryAdmin)