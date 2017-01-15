from django.contrib import admin
from .models import Part
# Register your models here.

class PartAdmin(admin.ModelAdmin):
    list_display = ('item_Number','item_Description')
    search_fields =['item_Number']
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


admin.site.register(Part,PartAdmin)
