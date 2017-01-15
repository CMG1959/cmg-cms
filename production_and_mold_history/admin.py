from django.contrib import admin

# Register your models here.
from .models import ProductionHistory, MoldHistory, MaintenanceRequests

class ProductionHistoryAdmin(admin.ModelAdmin):
    search_fields = ['dateCreated', 'jobNumber','inspectorName__EmpLName', 'descEvent','notifyToolroom']
    list_display = ('dateCreated', 'jobNumber', 'inspectorName', 'descEvent','notifyToolroom')
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

# class MaintenanceRequestAdmin(admin.ModelAdmin):
#     search_fields = ['dateCreated', 'jobNumber','inspectorName', 'descEvent']
#     list_display = ('dateCreated', 'jobNumber', 'inspectorName', 'descEvent')


class MoldHistoryAdmin(admin.ModelAdmin):
    search_fields = ['Date_Performed', 'moldNumber', 'inspectorName__EmpLName','pm', 'descEvent']
    list_display = ('Date_Performed', 'moldNumber', 'inspectorName','pm', 'descEvent')
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

admin.site.register(ProductionHistory, ProductionHistoryAdmin)
admin.site.register(MoldHistory, MoldHistoryAdmin)
# admin.site.register(MaintenanceRequests, MaintenanceRequestAdmin)

