from django.contrib import admin
from .models import Part
from django.db import models
# Register your models here.
from django.forms import TextInput, Textarea

class PartAdmin(admin.ModelAdmin):
    list_display = ('item_Number','item_Description')
    search_fields =['item_Number']
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


admin.site.register(Part,PartAdmin)
