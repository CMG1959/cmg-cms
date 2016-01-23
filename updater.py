from inspection.models import rangeInspection

for my_inspection in rangeInspection.objects.all():
    my_inspection.headCav = rangeInspection.headCavID