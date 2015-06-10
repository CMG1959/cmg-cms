from django.contrib import admin

# Register your models here.
from .models import partWeightInspection


class partWeightInspectionAdmin(admin.ModelAdmin):

    fields = ['jobID',
              'machineOperator',
              'inspectorName',
              'dateCreated',
              'cavityID',
              'partWeight']


admin.site.register(partWeightInspection,partWeightInspectionAdmin)