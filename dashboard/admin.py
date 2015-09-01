from django.contrib import admin

# Register your models here.
from .models import errorLog


class errorLogAdmin(admin.ModelAdmin):
    search_fields = ['shiftID','dateCreated','machNo','partDesc','jobID','inspectionName','errorDescription']
    list_display = ('shiftID','dateCreated','machNo','partDesc','jobID','inspectionName','errorDescription')


admin.site.register(errorLog,errorLogAdmin)