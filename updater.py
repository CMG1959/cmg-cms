from inspection.models import rangeInspection

for my_inspection in rangeInspection.objects.all():
    if rangeInspection.headCavID:
        my_inspection.headCav = rangeInspection.headCavID