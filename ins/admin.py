from django.contrib import admin

# Register your models here.
from .models import * 


class InspectionAdmin(admin.ModelAdmin):
    list_display =  ('production_date', 'shift', 'job_number',  'part_number',  'start_date_time')
    
 
class StepAdmin(admin.ModelAdmin):
    list_display = ('start_date_time',  'step_name',  'step_result')


class PropNumericLimitAdmin(admin.ModelAdmin):
    list_display = ('prop_tag',  'prop_value',  'low_limit',  'high_limit',  'cav_id')


class PropFloatAdmin(admin.ModelAdmin):
    list_display = ('prop_tag',  'prop_value')


class PropIntAdmin(admin.ModelAdmin):
    list_display = ('prop_tag',  'prop_value')


class PropBoolAdmin(admin.ModelAdmin):
    list_display = ('prop_tag',  'prop_value')
    

class PropTextAdmin(admin.ModelAdmin):
    list_display = ('prop_tag',  'prop_value')

class StaticInspectionGroupAdmin(admin.ModelAdmin):
    list_display = ('product_type',  'inspection_name_short')

class StaticInspectionAdmin(admin.ModelAdmin):
    list_display = ('static_inspection_group',  'tag_description_short')

class StaticInspectionLimitAdmin(admin.ModelAdmin):
    list_display = ('part_number',  'static_inspection',  'low_limit',  'high_limit')

class StaticInspectionBoolAdmin(admin.ModelAdmin):
    list_display = ('part_number',  'reason_long')


class StaticInspectionPartAdmin(admin.ModelAdmin):
    list_display = ('inspection_group', 'part_number')

admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(PropNumericLimit, PropNumericLimitAdmin)
admin.site.register(PropFloat, PropFloatAdmin)
admin.site.register(PropInt, PropIntAdmin)
admin.site.register(PropBool, PropBoolAdmin)
admin.site.register(PropText, PropTextAdmin)
admin.site.register(StaticInspectionGroup, StaticInspectionGroupAdmin)
admin.site.register(StaticInspection, StaticInspectionAdmin)
admin.site.register(StaticInspectionLimit, StaticInspectionLimitAdmin)
admin.site.register(StaticInspectionBool, StaticInspectionBoolAdmin)
admin.site.register(StaticInspectionPart, StaticInspectionPartAdmin)
