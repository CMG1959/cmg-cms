from django.contrib import admin

# Register your models here.
from .models import EquipmentType, EquipmentManufacturer, EquipmentInfo, PM, PMFreq, EquipmentPM, EquipmentRepair,\
    EquipmentClass

class EquipInfoAdmin(admin.ModelAdmin):
    search_fields = ['part_identifier']
    list_display = ('equipment_type', 'part_identifier','manufacturer_name')

class PMAdmin(admin.ModelAdmin):
    list_display = ('equipment_type','pm_frequency','pm_item')


class EquipmentPMAdmin(admin.ModelAdmin):
    search_fields = ['equipment_ID__part_identifier']
    list_display = ('employee','Date_Performed','equipment_ID','pm_frequency')

class EquipmentRepairAdmin(admin.ModelAdmin):
    search_fields = ['equipment_ID__part_identifier','po_num']
    list_display = ('employee','Date_Performed','equipment_ID','po_num')

class EquipmentTypeAdmin(admin.ModelAdmin):
    search_fields = ['equipment_type']
    list_display = ('equipment_class', 'equipment_type')

admin.site.register(EquipmentType, EquipmentTypeAdmin)

admin.site.register(EquipmentManufacturer)
admin.site.register(EquipmentInfo,EquipInfoAdmin)
admin.site.register(PM,PMAdmin)
admin.site.register(PMFreq)
admin.site.register(EquipmentPM,EquipmentPMAdmin)
admin.site.register(EquipmentRepair,EquipmentRepairAdmin)
admin.site.register(EquipmentClass)