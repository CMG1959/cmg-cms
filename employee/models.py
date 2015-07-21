from django.db import models

# Create your models here.

class JobTitles(models.Model):
    class Meta:
        verbose_name = 'Job Titles'
        verbose_name_plural = 'Organizations'

    JobNum = models.IntegerField(verbose_name='Job Number')
    JobTitle = models.CharField(verbose_name='Job Title', max_length=25)

    def __unicode__(self):
        return '%s' % (self.JobTitle)

class Employees(models.Model):
    class Meta:
        verbose_name = 'Employee Information'
        verbose_name_plural = 'Employee Information'

    EmpNum = models.CharField(verbose_name='Employee Number', max_length=25)
    EmpLName = models.CharField(verbose_name='Last Name', max_length=25, null=True)
    EmpFName = models.CharField(verbose_name='First Name', max_length=25, null=True)
    EmpManNum = models.CharField(verbose_name='Employee Man Number', max_length=25, null=True)
    EmpJob = models.ForeignKey('JobTitles',verbose_name='Employee Job Title')
    EmpShift = models.IntegerField(verbose_name='Shift', null=True)

    def __unicode__(self):
        return '%s - %s' % (self.EmpLName,self.EmpFName)
