from django.contrib import admin

# Register your models here.
from .models import *


class passFailTestAdmin(admin.ModelAdmin):
    search_fields = ['testName', 'isSystemInspection']
    list_display = ('testName', 'isSystemInspection')

class passFailTestCriteriaAdmin(admin.ModelAdmin):
    search_fields = ['testName','passFail']
    list_display = ('testName','passFail')

class passFailByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName','item_Number']
    list_display = ('testName','item_Number', 'inspections_per_shift')

class passFailInspectionAdmin(admin.ModelAdmin):
    search_fields = ['passFailTestName','jobID','dateCreated','inspectionResult']
    list_display = ('passFailTestName','jobID','dateCreated','inspectionResult')



class rangeTestAdmin(admin.ModelAdmin):
    search_fields = ['testName', 'isSystemInspection']
    list_display = ('testName', 'isSystemInspection')

class rangeTestByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName','item_Number']
    list_display = ('testName','item_Number', 'inspections_per_shift', 'rangeMin','rangeMax')


class rangeInspectionAdmin(admin.ModelAdmin):
    search_fields = ['rangeTestName','jobID','dateCreated','inspectionResult']
    list_display = ('rangeTestName','jobID','dateCreated','inspectionResult')




class textRecordAdmin(admin.ModelAdmin):
    search_fields = ['testName','requireAll', 'isSystemInspection']
    list_display = ('testName','requireAll', 'isSystemInspection')

class textRecordByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName','item_Number']
    list_display = ('testName','item_Number', 'inspections_per_shift')

class textInspectionAdmin(admin.ModelAdmin):
    search_fields = ['textTestName','jobID','dateCreated','inspectionResult']
    list_display = ('textTestName','jobID','dateCreated','inspectionResult')




class IntegerRecordAdmin(admin.ModelAdmin):
    search_fields = ['testName','requireAll', 'isSystemInspection']
    list_display = ('testName','requireAll', 'isSystemInspection')

class IntegerRecordByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName','item_Number']
    list_display = ('testName','item_Number', 'inspections_per_shift')

class IntegerInspectionAdmin(admin.ModelAdmin):
    search_fields = ['integerTestName','jobID','dateCreated','inspectionResult']
    list_display = ('integerTestName','jobID','dateCreated','inspectionResult')



class FloatRecordAdmin(admin.ModelAdmin):
    search_fields = ['testName', 'requireAll', 'isSystemInspection']
    list_display = ('testName', 'requireAll', 'isSystemInspection')

class FloatRecordByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName','item_Number']
    list_display = ('testName','item_Number', 'inspections_per_shift')

class FloatInspectionAdmin(admin.ModelAdmin):
    search_fields = ['floatTestName','jobID','dateCreated','inspectionResult']
    list_display = ('floatTestName','jobID','dateCreated','inspectionResult')




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


admin.site.register(IntegerRecord,IntegerRecordAdmin)
admin.site.register(IntegerRecordByPart,IntegerRecordByPartAdmin)
admin.site.register(IntegerInspection,IntegerInspectionAdmin)

admin.site.register(FloatRecord,FloatRecordAdmin)
admin.site.register(FloatRecordByPart,FloatRecordByPartAdmin)
admin.site.register(FloatInspection,FloatInspectionAdmin)