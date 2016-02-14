from django.contrib import admin

# Register your models here.
from .models import ProductionHistory, MoldHistory, MaintenanceRequests

class ProductionHistoryAdmin(admin.ModelAdmin):
    search_fields = ['dateCreated', 'jobNumber__jobNumber','inspectorName__EmpLName', 'descEvent','notifyToolroom']
    list_display = ('dateCreated', 'jobNumber', 'inspectorName', 'descEvent','notifyToolroom')


# class MaintenanceRequestAdmin(admin.ModelAdmin):
#     search_fields = ['dateCreated', 'jobNumber','inspectorName', 'descEvent']
#     list_display = ('dateCreated', 'jobNumber', 'inspectorName', 'descEvent')


class MoldHistoryAdmin(admin.ModelAdmin):
    search_fields = ['Date_Performed', 'moldNumber__mold_number', 'inspectorName__EmpLName','pm', 'descEvent']
    list_display = ('Date_Performed', 'moldNumber', 'inspectorName','pm', 'descEvent')

admin.site.register(ProductionHistory, ProductionHistoryAdmin)
admin.site.register(MoldHistory, MoldHistoryAdmin)
# admin.site.register(MaintenanceRequests, MaintenanceRequestAdmin)

