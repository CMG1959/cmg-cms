from django.contrib import admin

# Register your models here.

from .models import startUpShot, MattecProd


class startupShotAdmin(admin.ModelAdmin):
    list_display = ('item','jobNumber','dateCreated')
    fields = ['item',
              'jobNumber',
              'machNo',
              'shotWeight',
              'moldNumber',
              'activeCavities',
              'machineOperator',
              'inspectorName',
              ]
    search_fields = ['jobNumber','item__item_Number']


admin.site.register(startUpShot,startupShotAdmin)  # , ProductionAdmin)
admin.site.register(MattecProd)
