from django.contrib import admin

# Register your models here.
from .models import partWeightInspection, visualInspectionCriteria, visualInspection


class partWeightInspectionAdmin(admin.ModelAdmin):
    fields = ['jobID',
              'machineOperator',
              'inspectorName',
              'dateCreated',
              'cavityID',
              'partWeight']

class visualInspectionCriteriaAdmin(admin.ModelAdmin):
    fields = ['defectType']

class visualInspectionAdmin(admin.ModelAdmin):
    fields = ['jobID',
	'machineOperator',
	'inspectorName',
	'dateCreated',
	'inspectionResult',
	'defectType',
	'cavityID']

admin.site.register(partWeightInspection,partWeightInspectionAdmin)
admin.site.register(visualInspectionCriteria,visualInspectionCriteriaAdmin)
admin.site.register(visualInspection,visualInspectionAdmin)