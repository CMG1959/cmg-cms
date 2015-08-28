from django.contrib import admin
from .models import Part
# Register your models here.

class PartAdmin(admin.ModelAdmin):
    list_display = ('item_Number','item_Description')
    search_fields =['item_Number']



admin.site.register(Part,PartAdmin)
