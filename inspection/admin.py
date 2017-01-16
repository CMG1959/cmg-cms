from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
# Register your models here.
from inspection.models import *


class passFailTestAdmin(admin.ModelAdmin):
    search_fields = ['testName', 'isSystemInspection']
    list_display = ('testName', 'isSystemInspection')
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


class passFailTestCriteriaAdmin(admin.ModelAdmin):
    search_fields = ['testName__testName','passFail']
    list_display = ('testName','passFail')

    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


class passFailByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName__testName','item_Number__item_Number']
    list_display = ('testName','item_Number', 'inspections_per_shift')

    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

class passFailInspectionAdmin(admin.ModelAdmin):
    search_fields = ['passFailTestName__testName','jobID__jobNumber','dateCreated','inspectionResult']
    list_display = ('passFailTestName','jobID','dateCreated','inspectionResult')
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

class numericTestAdmin(admin.ModelAdmin):
    search_fields = ['testName', 'isSystemInspection']
    list_display = ('testName', 'isSystemInspection')
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

class numericTestByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName__testName','item_Number__item_Number']
    list_display = ('testName','item_Number', 'inspections_per_shift', 'rangeMin','rangeMax')
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

class numericInspectionAdmin(admin.ModelAdmin):
    search_fields = ['numericTestName__testName__testName','jobID__jobNumber','dateCreated','inspectionResult']
    list_display = ('numericTestName','jobID','dateCreated','inspectionResult')
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

class textRecordAdmin(admin.ModelAdmin):
    search_fields = ['testName','requireAll', 'isSystemInspection']
    list_display = ('testName','requireAll', 'isSystemInspection')
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

class textRecordByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName__testName','item_Number__item_Number']
    list_display = ('testName','item_Number', 'inspections_per_shift')

    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

class textInspectionAdmin(admin.ModelAdmin):
    search_fields = ['textTestName__testName','jobID__jobNumber','dateCreated','inspectionResult']
    list_display = ('textTestName','jobID','dateCreated','inspectionResult')
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


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
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

class rangeRecordByPartAdmin(admin.ModelAdmin):
    search_fields = ['testName__testName','item_Number__item_Number']
    list_display = ('testName','item_Number', 'inspections_per_shift')
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

class rangeInspectionAdmin(admin.ModelAdmin):
    search_fields = ['rangeTestName__testName','jobID__jobNumber','dateCreated','inspectionResult']
    list_display = ('rangeTestName','jobID','dateCreated','inspectionResult')
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }



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