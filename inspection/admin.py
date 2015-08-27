from django.contrib import admin

# Register your models here.
from .models import passFailTest, passFailTestCriteria, passFailByPart, passFailInspection


class passFailTestAdmin(admin.ModelAdmin):
    search_fields = ['testName']
    list_display = ('testName',)


class passFailTestCriteriaAdmin(admin.ModelAdmin):
    search_fields = ['testName','passFail']
    list_display = ('testName','passFail')

class passFailByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName','item_Number']
    list_display = ('testName','item_Number')

class passFailInspectionAdmin(admin.ModelAdmin):
    search_fields = ['passFailTestName','jobID','dateCreated','inspectionResult']
    list_display = ('passFailTestName','jobID','dateCreated','inspectionResult')


admin.site.register(passFailTest,passFailTestAdmin)
admin.site.register(passFailTestCriteria,passFailTestCriteriaAdmin)
admin.site.register(passFailByPart,passFailByPartAdmin)
admin.site.register(passFailInspection,passFailInspectionAdmin)

