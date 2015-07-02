from django.contrib import admin

# Register your models here.
from .models import ProductionHistory, MoldHistory

admin.site.register(ProductionHistory)
admin.site.register(MoldHistory)
