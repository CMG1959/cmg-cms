from django.contrib import admin

# Register your models here.
from .models import Mold

class MoldAdmin(admin.ModelAdmin):
    list_display = ('mold_number','mold_description')

    fields = ['mold_number',
              'mold_description',
              'num_cavities']

    search_fields = ['mold_number']


admin.site.register(Mold, MoldAdmin)
