from django.contrib import admin

# Register your models here.
from .models import EquipmentType, EquipmentManufacturer, EquipmentInfo

admin.site.register(EquipmentType)
admin.site.register(EquipmentManufacturer)
admin.site.register(EquipmentInfo)
