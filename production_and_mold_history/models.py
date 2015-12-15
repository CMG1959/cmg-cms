from django.db import models
from django.conf import settings
import uuid
# class YourAppConfig(AppConfig):
#     name = 'production_and_mold_history'
#     verbose_name = 'Production and Mold History Logs'
# # Create your models here.

class ProductionHistory(models.Model):
    class Meta:
        verbose_name = 'Production History Log Entry'
        verbose_name_plural = 'Production History Log Entries'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name")
    dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    jobNumber = models.CharField(max_length=20, verbose_name="Job Number", blank=True)
    descEvent = models.CharField(max_length=1000, verbose_name="Event Description")
    shift = models.IntegerField(verbose_name="Shift", null=True, blank=True)
    shortDate = models.DateField(verbose_name="Short Date", null=True, blank=True)
    notifyToolroom = models.BooleanField(verbose_name="Notify toolroom", default=False)

    def __unicode__(self):
        return '%s - %s: %s' % (self.dateCreated, self.jobNumber, self.descEvent)

class MaintenanceRequests(models.Model):
    class Meta:
        verbose_name = 'Maintenance Requests'
        verbose_name_plural = 'Maintenance Requests'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    inspectorName = models.CharField(max_length=20, verbose_name="Inspector Name")
    dateCreated = models.DateTimeField(verbose_name="Date Created")
    jobNumber = models.CharField(max_length=20, verbose_name="Job Number", blank=True)
    descEvent = models.CharField(max_length=1000, verbose_name="Event Description")
    shift = models.IntegerField(verbose_name="Shift", null=True, blank=True)
    shortDate = models.DateField(verbose_name="Short Date", null=True, blank=True)

    def __unicode__(self):
        return '%s - %s: %s' % (self.dateCreated, self.jobNumber, self.descEvent)



class MoldHistory(models.Model):
    class Meta:
        verbose_name = 'Mold History Log Entry'
        verbose_name_plural = 'Mold History Log Entries'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    inspectorName = models.CharField(max_length=20, verbose_name="Name")
    dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    moldNumber = models.CharField(max_length=12, verbose_name="Mold Number")
    descEvent = models.CharField(max_length=1000, verbose_name="Event Description")
    pm = models.BooleanField(default=False, verbose_name="Preventative Maintenance")
    repair = models.BooleanField(default=False, verbose_name="Repair")
    hours_worked = models.DecimalField(verbose_name="Hours worked", max_digits=10, decimal_places=2)
    loc_id = models.SmallIntegerField(verbose_name="Location ID",default=int(settings.PLANT_LOC))

    def __unicode__(self):
        return '%s - %s: %s' % (self.moldNumber, self.dateCreated, self.descEvent)
