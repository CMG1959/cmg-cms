from django.contrib import admin

# Register your models here.
from .models import passFailTest, passFailTestCriteria, passFailByPart, passFailInspection, rangeTest,\
    rangeTestByPart, rangeInspection,textRecord,textRecordByPart,textInspection


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


class rangeTestAdmin(admin.ModelAdmin):
    search_fields = ['testName']
    list_display = ('testName',)

class rangeTestByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName','item_Number']
    list_display = ('testName','item_Number','rangeMin','rangeMax')


class rangeInspectionAdmin(admin.ModelAdmin):
    search_fields = ['rangeTestName','jobID','dateCreated']
    list_display = ('rangeTestName','jobID','dateCreated')

class textRecordAdmin(admin.ModelAdmin):
    search_fields = ['testName','requireAll']
    list_display = ('testName','requireAll')

class textRecordByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName','item_Number']
    list_display = ('testName','item_Number')

class textInspectionAdmin(admin.ModelAdmin):
    search_fields = ['textTestName','jobID','dateCreated','inspectionResult']
    list_display = ('textTestName','jobID','dateCreated','inspectionResult')




admin.site.register(passFailTest,passFailTestAdmin)
admin.site.register(passFailTestCriteria,passFailTestCriteriaAdmin)
admin.site.register(passFailByPart,passFailByPartAdmin)
admin.site.register(passFailInspection,passFailInspectionAdmin)

admin.site.register(rangeTest,rangeTestAdmin)
admin.site.register(rangeTestByPart,rangeTestByPartAdmin)
admin.site.register(rangeInspection,rangeInspectionAdmin)

admin.site.register(textRecord,textRecordAdmin)
admin.site.register(textRecordByPart,textRecordByPartAdmin)
admin.site.register(textInspection,textInspectionAdmin)