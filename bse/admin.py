from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models

admin.site.register(models.users)
admin.site.register(models.share_owner)
admin.site.register(models.sell_data_table)