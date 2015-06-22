from django.contrib import admin

# Register your models here.

from .models import Production


class ProductionAdmin(admin.ModelAdmin):
    fields = ['item',
              'jobNumber',
              'machNo',
              'partWeight',
              'moldNumber',
              'headCavID',
              'activeCavities',
              'dateCreated',
              'inProduction']


admin.site.register(Production, ProductionAdmin)
