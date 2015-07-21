from django.contrib import admin

# Register your models here.
from .models import JobTitles,Employees

class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('JobNum','JobTitle')

class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('EmpNum','EmpLName','EmpFName','EmpShift')
    search_fields = ['EmpLName','EmpFName']

admin.site.register(JobTitles,JobTitleAdmin)
admin.site.register(Employees,EmployeesAdmin)