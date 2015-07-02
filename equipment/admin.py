from django.contrib import admin

# Register your models here.
from .models import EquipmentType, EquipmentManufacturer, EquipmentInfo, PM, PMFreq, EquipmentPM, EquipmentRepair

admin.site.register(EquipmentType)
admin.site.register(EquipmentManufacturer)
admin.site.register(EquipmentInfo)
admin.site.register(PM)
admin.site.register(PMFreq)
admin.site.register(EquipmentPM)
admin.site.register(EquipmentRepair)
