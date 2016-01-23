from inspection.models import rangeInspection, passFailInspection, textInspection

for my_inspection in rangeInspection.objects.all():
    if rangeInspection.headCavID:
        my_inspection.headCav = rangeInspection.headCavID


for my_inspection in passFailInspection.objects.all():
    if rangeInspection.headCavID:
        my_inspection.headCav = rangeInspection.headCavID


for my_inspection in textInspection.objects.all():
    if rangeInspection.headCavID:
        my_inspection.headCav = rangeInspection.headCavID