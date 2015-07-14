from django.db import models
# from molds.models import Mold, PartIdentifier
# Create your models here.



class startUpShot(models.Model):
    class Meta:
        verbose_name = 'Startup Shot'
        verbose_name_plural = 'Startup Shots'

    item = models.ForeignKey('part.Part', verbose_name="Item")
    jobNumber = models.CharField(max_length=15, unique=True, verbose_name="Job Number")
    moldNumber = models.ForeignKey('molds.Mold', verbose_name="Mold Number")
    activeCavities = models.IntegerField(verbose_name="Active Cavities")
    dateCreated = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    machNo = models.ForeignKey('equipment.EquipmentInfo', verbose_name="Machine Number")
    inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name")
    shotWeight = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Shot Weight")
    cycleTime = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Cycle Time (s)")

    def __unicode__(self):
        return self.jobNumber


class MattecProd(models.Model):
    class Meta:
        verbose_name = 'MATTEC Current Job Information'
        verbose_name_plural = 'MATTEC Current Job Information'

    ### This information will be taken from MATTEC via SQL script
    jobNumber = models.CharField(max_length=15, verbose_name="Job Number")
    machNo = models.CharField(max_length=10, verbose_name="Machine Number")
    itemDesc = models.CharField(max_length=50, verbose_name="Item Description")
    itemNo = models.CharField(max_length=15, verbose_name="Item Number")
    moldNumber = models.CharField(max_length=15, verbose_name="Mold Number")
    activeCavities = models.IntegerField(verbose_name="Active Cavities")
    cycleTime = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Cycle Time (s)")

    def __unicode__(self):
        return '%s - %s' % (self.machNo, self.itemDesc)
