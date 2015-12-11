from django.contrib import admin

# Register your models here.
from .models import ProductionHistory, MoldHistory

class ProductionHistoryAdmin(admin.ModelAdmin):
    search_fields = ['dateCreated', 'jobNumber','inspectorName', 'descEvent']
    list_display = ('dateCreated', 'jobNumber', 'inspectorName', 'descEvent')

class MoldHistoryAdmin(admin.ModelAdmin):
    search_fields = ['dateCreated', 'moldNumber', 'inspectorName','pm', 'descEvent']
    list_display = ('dateCreated', 'moldNumber', 'inspectorName','pm', 'descEvent')

admin.site.register(ProductionHistory, ProductionHistoryAdmin)
admin.site.register(MoldHistory, MoldHistoryAdmin)
