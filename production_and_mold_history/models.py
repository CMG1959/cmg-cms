from django.db import models

# Create your models here.

class ProductionHistory(models.Model):
    inspectorName = models.ForeignKey('employee.employee', verbose_name="Inspector Name")
    dateCreated = models.DateTimeField(verbose_name="Date Created",auto_now_add=True)
    jobNumber = models.ForeignKey('startupshot.Production',verbose_name="Job Number")
    descEvent = models.CharField(max_length=None,verbose_name="Event Description")


class MoldHistory(models.Model):
    inspectorName = models.ForeignKey('employee.employee', verbose_name="Name")
    dateCreated = models.DateTimeField(verbose_name="Date Created",auto_now_add=True)
    moldNumber = models.ForeignKey('molds.Mold',verbose_name="Mold Number")
    descEvent = models.CharField(max_length=None,verbose_name="Event Description")
    pm = models.BooleanField(default=False,verbose_name="Preventative Maintenance")
    repair = models.BooleanField(default=False,verbose_name="Repair")
    hours_worked = models.DecimalField(verbose_name="Hours worked",max_digits=10,decimal_places=2)
