from inspection.models import rangeInspection, passFailInspection, textInspection

for my_inspection in rangeInspection.objects.filter(headCavID__isnull=False):
    if my_inspection.headCavID:
        my_inspection.headCav = '%s - %s'% (my_inspection.headCavID.head_code.upper()
                                            ,my_inspection.headCavID.cavity_id.capitalize())
        my_inspection.save()


for my_inspection in passFailInspection.objects.filter(headCavID__isnull=False):
    if my_inspection.headCavID:
        my_inspection.headCav = '%s - %s'% (my_inspection.headCavID.head_code.upper()
                                            ,my_inspection.headCavID.cavity_id.capitalize())
        my_inspection.save()


for my_inspection in textInspection.objects.filter(headCavID__isnull=False):

    if my_inspection.headCavID:
        my_inspection.headCav = '%s - %s'% (my_inspection.headCavID.head_code.upper()
                                            ,my_inspection.headCavID.cavity_id.capitalize())
        my_inspection.save()