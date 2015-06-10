from django.contrib import admin

# Register your models here.
from .models import cimc_organizations, employee


class CIMC_EmplopyeeAdmin(admin.ModelAdmin):
    fields = ['last_name',
              'first_name',
              'employee_id',
              'organization_name']

admin.site.register(cimc_organizations)
admin.site.register(employee,CIMC_EmplopyeeAdmin)