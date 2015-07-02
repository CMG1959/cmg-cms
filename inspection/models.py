from datetime import datetime

from django.db import models



# Create your models here.
class visualInspectionCriteria(models.Model):
    class Meta:
        verbose_name = 'Visual Inspection Criterion'
        verbose_name_plural = 'Visual Inspection Criteria'

    defectType = models.CharField(max_length=25)

    def __unicode__(self):
        return self.defectType


class partWeightInspection(models.Model):
    class Meta:
        verbose_name = 'Part Weight Inspection'
        verbose_name_plural = 'Part Weight Inspections'

    jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='pwi_jobID')
    machineOperator = models.ForeignKey('employee.employee', verbose_name="Machine Operator",
                                        related_name='pwi_machineOperator')
    inspectorName = models.ForeignKey('employee.employee', verbose_name="Inspector Name",
                                      related_name='pwi_inspectorName')
    dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    headCavID = models.ForeignKey('molds.PartIdentifier', verbose_name="Head and Cavity ID")
    partWeight = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Part Weight")

    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)


class shotWeightInspection(models.Model):
    class Meta:
        verbose_name = 'Shot Weight Inspection'
        verbose_name_plural = 'Shot Weight Inspections'

    jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='swi_jobID')
    machineOperator = models.ForeignKey('employee.employee', verbose_name="Machine Operator",
                                        related_name='swi_machineOperator')
    inspectorName = models.ForeignKey('employee.employee', verbose_name="Inspector Name",
                                      related_name='swi_inspectorName')
    dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    shotWeight = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Shot Weight")

    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)


class visualInspection(models.Model):
    class Meta:
        verbose_name = 'Visual Inspection'
        verbose_name_plural = 'Visual Inspections'

    jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='vi_jobID')
    machineOperator = models.ForeignKey('employee.employee', verbose_name="Machine Operator",
                                        related_name='vi_machineOperator')
    inspectorName = models.ForeignKey('employee.employee', verbose_name="Inspector Name",
                                      related_name='vi_inspectorName')
    dateCreated = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    inspectionResult = models.BooleanField(verbose_name="Inspection Result")
    defectType = models.ManyToManyField(visualInspectionCriteria, verbose_name="Defect Type")
    headCavID = models.ForeignKey('molds.PartIdentifier', verbose_name="Head and Cavity ID")

    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)
