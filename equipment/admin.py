from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
# Register your models here.
from .models import EquipmentType, EquipmentManufacturer, EquipmentInfo, PM, PMFreq, EquipmentPM, EquipmentRepair,\
    EquipmentClass

class EquipInfoAdmin(admin.ModelAdmin):
    search_fields = ['part_identifier']
    list_display = ('part_identifier', 'equipment_type', 'manufacturer_name')

class PMAdmin(admin.ModelAdmin):
    list_display = ('equipment_type', 'pm_frequency', 'pm_item')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

class EquipmentPMAdmin(admin.ModelAdmin):
    search_fields = ['equipment_ID__part_identifier']
    list_display = ('Date_Performed', 'equipment_ID', 'employee', 'pm_frequency')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


class EquipmentRepairAdmin(admin.ModelAdmin):
    search_fields = ['equipment_ID__part_identifier','po_num']
    list_display = ('Date_Performed', 'equipment_ID',  'employee', 'po_num')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

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