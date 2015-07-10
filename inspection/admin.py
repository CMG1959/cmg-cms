from django.contrib import admin

# Register your models here.
from .models import partWeightInspection, visualInspectionCriteria, visualInspection, shotWeightInspection, \
    outsideDiameterInspection, volumeInspection, neckDiameterInspection, assemblyTestCriteria, \
    assemblyTest, assemblyInspection, cartonTemperature, visionTestCriteria, visionTest, \
    visionInspection


class partWeightInspectionAdmin(admin.ModelAdmin):
    fields = ['jobID',
              'machineOperator',
              'inspectorName',
              'dateCreated',
              'headCavID',
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
              'headCavID']


admin.site.register(partWeightInspection, partWeightInspectionAdmin)
admin.site.register(visualInspectionCriteria, visualInspectionCriteriaAdmin)
admin.site.register(visualInspection, visualInspectionAdmin)

admin.site.register(shotWeightInspection)
admin.site.register(outsideDiameterInspection)
admin.site.register(volumeInspection)
admin.site.register(neckDiameterInspection)
admin.site.register(assemblyTestCriteria)
admin.site.register(assemblyTest)
admin.site.register(assemblyInspection)
admin.site.register(cartonTemperature)
admin.site.register(visionTestCriteria)
admin.site.register(visionTest)
admin.site.register(visionInspection)
