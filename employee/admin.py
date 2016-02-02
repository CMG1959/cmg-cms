from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from employee.models import Employees, WebAppEmployee, EmployeeAtWorkstation

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmployeeInline(admin.StackedInline):
    model = WebAppEmployee
    can_delete = False
    verbose_name_plural = 'Web App User'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('EmpNum','EmpLName','EmpFName','EmpShift','StatusActive')
    search_fields = ['EmpLName','EmpFName']

admin.site.register(Employees,EmployeesAdmin)

class EmployeeAtWorkstationAdmin(admin.ModelAdmin):
    ordering = ['workstation']
    list_display = ('workstation', 'employee')
    search_fields = ['workstation', 'employee']

admin.site.register(EmployeeAtWorkstation, EmployeeAtWorkstationAdmin)