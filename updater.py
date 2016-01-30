# from inspection.models import rangeInspection, passFailInspection, textInspection
#
# for my_inspection in rangeInspection.objects.filter(headCavID__isnull=False):
#     if my_inspection.headCavID:
#         my_inspection.headCav = '%s - %s'% (my_inspection.headCavID.head_code.upper()
#                                             ,my_inspection.headCavID.cavity_id.capitalize())
#         my_inspection.save()
#
#
# for my_inspection in passFailInspection.objects.filter(headCavID__isnull=False):
#     if my_inspection.headCavID:
#         my_inspection.headCav = '%s - %s'% (my_inspection.headCavID.head_code.upper()
#                                             ,my_inspection.headCavID.cavity_id.capitalize())
#         my_inspection.save()
#
#
# for my_inspection in textInspection.objects.filter(headCavID__isnull=False):
#
#     if my_inspection.headCavID:
#         my_inspection.headCav = '%s - %s'% (my_inspection.headCavID.head_code.upper()
#                                             ,my_inspection.headCavID.cavity_id.capitalize())
#         my_inspection.save()

from employee.models import WebAppEmployee, Employees
from django.contrib.auth.models import User

for employee in Employees.objects.all():
    try:
        fname = employee.EmpFName
        lname = employee.EmpLName
        man_num = employee.EmpManNum

        user_obj = User.objects.get(first_name=fname,last_name=lname)

        web_app_user = WebAppEmployee(user=user_obj,EmpManNum=man_num)
        web_app_user.save()
    except Exception as e:
        print str(e)