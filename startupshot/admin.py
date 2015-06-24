from django.contrib import admin

# Register your models here.

from .models import Production, MattecProd


class ProductionAdmin(admin.ModelAdmin):
    fields = ['item',
              'jobNumber',
              'machNo',
              'shotWeight',
              'moldNumber',
              'activeCavities',
              'dateCreated',
              'inspectorName',
              'inProduction']


admin.site.register(Production)#, ProductionAdmin)
admin.site.register(MattecProd)
