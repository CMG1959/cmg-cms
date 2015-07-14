from django.db import models

# class YourAppConfig(AppConfig):
#     name = 'production_and_mold_history'
#     verbose_name = 'Production and Mold History Logs'
# # Create your models here.

class ProductionHistory(models.Model):
    class Meta:
        verbose_name = 'Production History Log Entry'
        verbose_name_plural = 'Production History Log Entries'

    inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name")
    dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    jobNumber = models.ForeignKey('startupshot.startUpShot', verbose_name="Job Number")
    descEvent = models.CharField(max_length=1000, verbose_name="Event Description")

    def __unicode__(self):
        return '%s - %s' % (self.jobNumber, self.dateCreated)


class MoldHistory(models.Model):
    class Meta:
        verbose_name = 'Mold History Log Entry'
        verbose_name_plural = 'Mold History Log Entries'

    inspectorName = models.ForeignKey('employee.Employees', verbose_name="Name")
    dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    moldNumber = models.ForeignKey('molds.Mold', verbose_name="Mold Number")
    descEvent = models.CharField(max_length=1000, verbose_name="Event Description")
    pm = models.BooleanField(default=False, verbose_name="Preventative Maintenance")
    repair = models.BooleanField(default=False, verbose_name="Repair")
    hours_worked = models.DecimalField(verbose_name="Hours worked", max_digits=10, decimal_places=2)

    def __unicode__(self):
        return '%s - %s' % (self.moldNumber, self.dateCreated)