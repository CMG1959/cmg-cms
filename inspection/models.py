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
    inspectionResult = models.BooleanField(verbose_name="Inspection Result (check if passed)")
    defectType = models.ManyToManyField(visualInspectionCriteria, verbose_name="Defect Type")
    headCavID = models.ForeignKey('molds.PartIdentifier', verbose_name="Head and Cavity ID")

    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)


class outsideDiameterInspection(models.Model):
    class Meta:
        verbose_name = 'Outside Diameter Inspection'
        verbose_name_plural = 'Outside Diameter Inspections'

    jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='odi_jobID')
    machineOperator = models.ForeignKey('employee.employee', verbose_name="Machine Operator",
                                        related_name='odi_machineOperator')
    inspectorName = models.ForeignKey('employee.employee', verbose_name="Inspector Name",
                                      related_name='odi_inspectorName')
    dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    outsideDiameter = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Outside Diameter")

    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)


class volumeInspection(models.Model):
    class Meta:
        verbose_name = 'Volume Inspection'
        verbose_name_plural = 'Volume Inspections'

    jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='vol_jobID')
    machineOperator = models.ForeignKey('employee.employee', verbose_name="Machine Operator",
                                        related_name='vol_machineOperator')
    inspectorName = models.ForeignKey('employee.employee', verbose_name="Inspector Name",
                                      related_name='vol_inspectorName')
    dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    liquidWeight = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Liquid Weight (g)")

    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)


class neckDiameterInspection(models.Model):
    class Meta:
        verbose_name = 'Neck Diameter Inspection'
        verbose_name_plural = 'Neck Diameter Inspections'

    jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='ndi_jobID')
    machineOperator = models.ForeignKey('employee.employee', verbose_name="Machine Operator",
                                        related_name='ndi_machineOperator')
    inspectorName = models.ForeignKey('employee.employee', verbose_name="Inspector Name",
                                      related_name='ndi_inspectorName')
    dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    testResult = models.BooleanField(verbose_name="Test Result", default=True)

    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)



class assemblyTestCriteria(models.Model):
    class Meta:
        verbose_name = 'Assembly Test Criteria'
        verbose_name_plural = 'Assembly Test Criteria'

    assemblyTest = models.CharField(max_length=25, verbose_name="Test type")

    def __unicode__(self):
        return self.assemblyTest


class assemblyTest(models.Model):
    class Meta:
        verbose_name = 'Assembly Test Criteria by Model'
        verbose_name_plural = 'Assembly Test Criteria by Model'

    part = models.ForeignKey('part.Part')
    assemblyTestItem = models.ForeignKey(assemblyTestCriteria)

    def __unicode__(self):
        return self.assemblyTestItem.assemblyTest


class assemblyInspection(models.Model):
    class Meta:
        verbose_name = 'Assembly Inspection'
        verbose_name_plural = 'Assembly Inspections'

    jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='assem_jobID')
    machineOperator = models.ForeignKey('employee.employee', verbose_name="Machine Operator",
                                        related_name='assem_machineOperator')
    inspectorName = models.ForeignKey('employee.employee', verbose_name="Inspector Name",
                                      related_name='assem_inspectorName')
    dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    assemblyTestResults = models.ManyToManyField(assemblyTest, verbose_name="Assembly Test Results")

    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)


class cartonTemperature(models.Model):
    class Meta:
        verbose_name = 'Carton Temperature'
        verbose_name_plural = 'Carton Temperatures'

    jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='ct_jobID')
    machineOperator = models.ForeignKey('employee.employee', verbose_name="Machine Operator",
                                        related_name='ct_machineOperator')
    inspectorName = models.ForeignKey('employee.employee', verbose_name="Inspector Name",
                                      related_name='ct_inspectorName')
    dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    cartonTemp = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Carton Temp (F)")

    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)


class visionTestCriteria(models.Model):
    class Meta:
        verbose_name = 'Vision Test Criteria'
        verbose_name_plural = 'Vision Test Criteria'

    visionTest = models.CharField(max_length=25, verbose_name="Test type")

    def __unicode__(self):
        return self.visionTest


class visionTest(models.Model):
    class Meta:
        verbose_name = 'Vision Test Criteria by Model'
        verbose_name_plural = 'Vision Test Criteria by Model'

    equipmentID = models.ForeignKey('equipment.EquipmentInfo')
    visionTestItem = models.ForeignKey(visionTestCriteria)

    def __unicode__(self):
        return self.assemblyTestItem.assemblyTest


class visionInspection(models.Model):
    class Meta:
        verbose_name = 'Vision System Test'
        verbose_name_plural = 'Vision System Test'

    jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='vis_jobID')
    machineOperator = models.ForeignKey('employee.employee', verbose_name="Machine Operator",
                                        related_name='vis_machineOperator')
    inspectorName = models.ForeignKey('employee.employee', verbose_name="Inspector Name",
                                      related_name='vis_inspectorName')
    dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    visionTestResults = models.ManyToManyField(visionTest, verbose_name="Vision System Test Results")

    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)
