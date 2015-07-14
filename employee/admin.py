from django.contrib import admin

# Register your models here.
from .models import JobTitles,Employees

admin.site.register(JobTitles)
admin.site.register(Employees)