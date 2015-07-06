from django.contrib import admin

# Register your models here.
from .models import organizations, employee


class CIMC_EmplopyeeAdmin(admin.ModelAdmin):
    fields = ['last_name',
              'first_name',
              'employee_id',
              'organization_name',
              'shift_id']


admin.site.register(organizations)
admin.site.register(employee, CIMC_EmplopyeeAdmin)
