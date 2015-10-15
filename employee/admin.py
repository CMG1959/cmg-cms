from django.contrib import admin

# Register your models here.
from .models import Employees

class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('EmpNum','EmpLName','EmpFName','EmpShift')
    search_fields = ['EmpLName','EmpFName']

admin.site.register(Employees,EmployeesAdmin)