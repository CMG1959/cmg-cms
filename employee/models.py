from django.db import models
from django.contrib.auth.models import User

class WebAppEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    EmpManNum = models.IntegerField(verbose_name='Employee Man Number', null=True)


class Employees(models.Model):
    class Meta:
        verbose_name = 'Employee Information'
        verbose_name_plural = 'Employee Information'

    EmpNum = models.IntegerField(verbose_name='Employee Number', null=True)
    EmpLName = models.CharField(verbose_name='Last Name', max_length=50, null=True)
    EmpFName = models.CharField(verbose_name='First Name', max_length=50, null=True)
    EmpLMName = models.CharField(verbose_name='Alias', max_length=20, null=True, default=' ')
    EmpManNum = models.IntegerField(verbose_name='Employee Man Number', null=True)
    EmpShift = models.CharField(verbose_name='Shift', max_length=1, null=True)
    StatusActive =  models.BooleanField(verbose_name="Status Active",default=True)
    IsAdmin = models.BooleanField(verbose_name="Is Admin",default=False)
    IsQCStaff = models.BooleanField(verbose_name="Is QC Staff",default=False)
    IsMgmtStaff = models.BooleanField(verbose_name="Is Mgmt Staff",default=False)
    IsSupervStaff = models.BooleanField(verbose_name="Is Supervisor Staff",default=False)
    IsOpStaff = models.BooleanField(verbose_name="Is Ops Staff",default=False)
    IsToolStaff = models.BooleanField(verbose_name="Is Tool Staff",default=False)
    IsMaintStaff = models.BooleanField(verbose_name="Is Maint Staff",default=False)
    IsPTLStaff = models.BooleanField(verbose_name="Is PTL Staff",default=False)
    DeviceToken = models.CharField(verbose_name='User GUID', null=True, max_length=36)
    DevTokenExpires = models.DateTimeField(verbose_name='Device Expire', null=True)

    def __unicode__(self):
        return '%s - %s' % (self.EmpLName,self.EmpFName)
