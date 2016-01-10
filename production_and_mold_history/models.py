from django.db import models
from django.conf import settings
import uuid


class ProductionHistory(models.Model):
    class Meta:
        verbose_name = 'Production History Log Entry'
        verbose_name_plural = 'Production History Log Entries'
        managed = False

    inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name")
    dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    dateCreatedL = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    jobNumber = models.CharField(max_length=20, verbose_name="Job Number", blank=True)
    descEvent = models.CharField(max_length=1000, verbose_name="Event Description")
    Prod_shift = models.IntegerField(verbose_name="Shift", null=True, blank=True)
    Prod_Date = models.DateField(verbose_name="Short Date", null=True, blank=True)
    notifyToolroom = models.BooleanField(verbose_name="Notify toolroom", default=False)
    STA_Reported = models.IntegerField(verbose_name='Reported Workstation',default=0, blank=True)

    def __unicode__(self):
        return '%s - %s: %s' % (self.dateCreated, self.jobNumber, self.descEvent)

class MaintenanceRequests(models.Model):
    class Meta:
        verbose_name = 'Maintenance Requests'
        verbose_name_plural = 'Maintenance Requests'
        managed = False
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    Requestor_Name = models.CharField(max_length=20, verbose_name="Requestor Name")
    Request_Time = models.DateTimeField(verbose_name="Date Requested", auto_now_add=True)
    Request_Shift = models.SmallIntegerField(verbose_name='Shift')
    Request_Loc = models.SmallIntegerField(verbose_name= 'Request Location')
    Request_Source = models.SmallIntegerField(verbose_name= 'Request Location')
    Tool_id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    Tool_Number = models.CharField(max_length=20, verbose_name="Tool Number")
    Request_Desc = models.CharField(max_length=1000, verbose_name="Request Description")
    Ack_Acknowledged = models.BooleanField(verbose_name="Ackknowledged", default=False)
    Ack_Time =  models.DateTimeField(verbose_name="Date Acknowledged", auto_now_add=True)
    Ack_Name =  models.CharField(max_length=20, verbose_name="Acknowledger Name")
    Ack_Notes =  models.CharField(max_length=1000, verbose_name="Acknowledger Comments")
    Ack_Link_WO = models.IntegerField(verbose_name="WO")

    def __unicode__(self):
        return '%s - %s' % (self.Tool_Number, self.Requestor_Name)



class MoldHistory(models.Model):
    class Meta:
        verbose_name = 'Mold History Log Entry'
        verbose_name_plural = 'Mold History Log Entries'
        managed = False
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    parent_id = models.CharField(max_length=36,default=uuid.uuid4,editable=False)
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
