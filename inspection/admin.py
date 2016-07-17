from django.contrib import admin

# Register your models here.
from inspection.models import *


class passFailTestAdmin(admin.ModelAdmin):
    search_fields = ['testName', 'isSystemInspection']
    list_display = ('testName', 'isSystemInspection')

class passFailTestCriteriaAdmin(admin.ModelAdmin):
    search_fields = ['testName__testName','passFail']
    list_display = ('testName','passFail')

class passFailByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName__testName','item_Number__item_Number']
    list_display = ('testName','item_Number', 'inspections_per_shift')

class passFailInspectionAdmin(admin.ModelAdmin):
    search_fields = ['passFailTestName__testName','jobID__jobNumber','dateCreated','inspectionResult']
    list_display = ('passFailTestName','jobID','dateCreated','inspectionResult')



class numericTestAdmin(admin.ModelAdmin):
    search_fields = ['testName', 'isSystemInspection']
    list_display = ('testName', 'isSystemInspection')

class numericTestByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName__testName','item_Number__item_Number']
    list_display = ('testName','item_Number', 'inspections_per_shift', 'rangeMin','rangeMax')


class numericInspectionAdmin(admin.ModelAdmin):
    search_fields = ['rangeTestName__testName__testName','jobID__jobNumber','dateCreated','inspectionResult']
    list_display = ('numericTestName','jobID','dateCreated','inspectionResult')




class textRecordAdmin(admin.ModelAdmin):
    search_fields = ['testName','requireAll', 'isSystemInspection']
    list_display = ('testName','requireAll', 'isSystemInspection')

class textRecordByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName__testName','item_Number__item_Number']
    list_display = ('testName','item_Number', 'inspections_per_shift')

class textInspectionAdmin(admin.ModelAdmin):
    search_fields = ['textTestName__testName','jobID__jobNumber','dateCreated','inspectionResult']
    list_display = ('textTestName','jobID','dateCreated','inspectionResult')



#
# class IntegerRecordAdmin(admin.ModelAdmin):
#     search_fields = ['testName','requireAll', 'isSystemInspection']
#     list_display = ('testName','requireAll', 'isSystemInspection')
#
# class IntegerRecordByPartAdmin(admin.ModelAdmin):
#     search_fields = ['testName__testName','item_Number__item_Number']
#     list_display = ('testName','item_Number', 'inspections_per_shift')
#
# class IntegerInspectionAdmin(admin.ModelAdmin):
#     search_fields = ['integerTestName__testName','jobID__jobNumber','dateCreated','inspectionResult']
#     list_display = ('integerTestName','jobID','dateCreated','inspectionResult')



class rangeRecordAdmin(admin.ModelAdmin):
    search_fields = ['testName', 'requireAll', 'isSystemInspection']
    list_display = ('testName', 'requireAll', 'isSystemInspection')

class rangeRecordByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName__testName','item_Number__item_Number']
    list_display = ('testName','item_Number', 'inspections_per_shift')

class rangeInspectionAdmin(admin.ModelAdmin):
    search_fields = ['rangeTestName__testName','jobID__jobNumber','dateCreated','inspectionResult']
    list_display = ('rangeTestName','jobID','dateCreated','inspectionResult')




admin.site.register(passFailTest,passFailTestAdmin)
admin.site.register(passFailTestCriteria,passFailTestCriteriaAdmin)
admin.site.register(passFailByPart,passFailByPartAdmin)
admin.site.register(passFailInspection,passFailInspectionAdmin)

admin.site.register(numericTest, numericTestAdmin)
admin.site.register(numericTestByPart, numericTestByPartAdmin)
admin.site.register(numericInspection, numericInspectionAdmin)

admin.site.register(textRecord,textRecordAdmin)
admin.site.register(textRecordByPart,textRecordByPartAdmin)
admin.site.register(textInspection,textInspectionAdmin)


# admin.site.register(IntegerRecord,IntegerRecordAdmin)
# admin.site.register(IntegerRecordByPart,IntegerRecordByPartAdmin)
# admin.site.register(IntegerInspection,IntegerInspectionAdmin)

admin.site.register(RangeRecord, rangeRecordAdmin)
admin.site.register(RangeRecordByPart, rangeRecordByPartAdmin)
admin.site.register(RangeInspection, rangeInspectionAdmin)