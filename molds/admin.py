from django.contrib import admin

# Register your models here.
from .models import Mold, PartIdentifier


class PartIdentifierInline(admin.StackedInline):
    model = PartIdentifier


class MoldAdmin(admin.ModelAdmin):
    fields = ['mold_number',
              'mold_description',
              'num_cavities']

    inlines = [PartIdentifierInline]

    search_fields = ['mold_number']


admin.site.register(Mold, MoldAdmin)
