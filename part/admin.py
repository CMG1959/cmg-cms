from django.contrib import admin
from .models import Part, PartInspection
# Register your models here.

class PartAdmin(admin.ModelAdmin):
    list_display = ('item_Number','item_Description')
    search_fields =['item_Number']


class PartInspectionAdmin(admin.ModelAdmin):

    search_fields =['item_Number__item_Number']

admin.site.register(Part,PartAdmin)
admin.site.register(PartInspection,PartInspectionAdmin)
