from django.db import models

# Create your models here.

class Employees(models.Model):
    class Meta:
        verbose_name = 'Employee Information'
        verbose_name_plural = 'Employee Information'

    EmpNum = models.IntegerField(verbose_name='Employee Number', null=True)
    EmpLName = models.CharField(verbose_name='Last Name', max_length=25, null=True)
    EmpFName = models.CharField(verbose_name='First Name', max_length=25, null=True)
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

    def __unicode__(self):
        return '%s - %s' % (self.EmpLName,self.EmpFName)
