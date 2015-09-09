from datetime import datetime

from django.db import models



# Create your models here.


#######################################################################################################################
#
#
# Pass Fail Inspection
#
#
#######################################################################################################################

class passFailTest(models.Model):
    class Meta:
        verbose_name = 'Name - Pass Fail Test'
        verbose_name_plural = 'Name - Pass Fail Test'

    testName = models.CharField(max_length=75, verbose_name="Pass Fail Test Name",unique=True)
    requireAll = models.BooleanField(verbose_name="Require all parts get inspection?",default=False)

    def __unicode__(self):
        return '%s' % (self.testName)

class passFailTestCriteria(models.Model):
    class Meta:
        verbose_name = 'Criteria - Pass Fail Test'
        verbose_name_plural = 'Criteria - Pass Fail Test'
        unique_together = ("testName", "passFail")

    testName = models.ForeignKey('passFailTest', verbose_name = "Pass Fail Test Name")
    passFail = models.CharField(max_length=75, verbose_name = "Pass Fail Reason")

    def __unicode__(self):
        return '%s' % (self.passFail)

class passFailByPart(models.Model):
    class Meta:
        verbose_name = 'Part Assignment - Pass Fail Test'
        verbose_name_plural = 'Part Assignment - Pass Fail Tests'
        unique_together = ("testName", "item_Number")


    testName = models.ForeignKey('passFailTest', verbose_name = "Pass Fail Test Name")
    item_Number = models.ForeignKey('part.Part', verbose_name = "Part Number")

    def __unicode__(self):
        return '%s - %s' % (self.testName, self.item_Number)

class passFailInspection(models.Model):
    class Meta:
        verbose_name = 'Record - Pass Fail Inspection'
        verbose_name_plural = 'Record - Pass Fail Inspections'

    passFailTestName = models.ForeignKey('passFailTest',verbose_name='Inspection Name')
    jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='pf_jobID')
    machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
                                        related_name='pf_machineOperator')
    inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
                                      related_name='pf_inspectorName')
    dateCreated = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    inspectionResult = models.BooleanField(verbose_name="Inspection Result (check if passed)",default=True)
    defectType = models.ManyToManyField('passFailTestCriteria', verbose_name="Defect Type",  blank=True)
    headCavID = models.ForeignKey('molds.PartIdentifier', verbose_name="Head and Cavity ID", blank=True, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)


#######################################################################################################################
#
#
# Range Inspection
#
#
#######################################################################################################################

class rangeTest(models.Model):
    class Meta:
        verbose_name = 'Name - Range Test'
        verbose_name_plural = 'Name - Range Test'

    testName = models.CharField(max_length=75, verbose_name="Range Test Name",unique=True)
    requireAll = models.BooleanField(verbose_name="Require all parts get inspection?",default=False)
    calcAvg = models.BooleanField(verbose_name="Report raw data (do not take average)?",default=False)

    def __unicode__(self):
        return '%s' % (self.testName)

class rangeTestByPart(models.Model):
    class Meta:
        verbose_name = 'Part Assignment - Range Test Parameters'
        verbose_name_plural = 'Part Assignment - Range Test Parameters'
        unique_together = ("testName", "item_Number")

    testName = models.ForeignKey('rangeTest', verbose_name = "Range Test Name")
    item_Number = models.ForeignKey('part.Part', verbose_name = "Part Number")
    rangeMin = models.DecimalField(verbose_name="Minimum Value", default=0, max_digits=12,decimal_places=3)
    rangeMax = models.DecimalField(verbose_name="Maximum Value", default=9999999, max_digits=12,decimal_places=3)

    def __unicode__(self):
        return '%s' % (self.testName)

class rangeInspection(models.Model):
    class Meta:
        verbose_name = 'Record - Range Inspection'
        verbose_name_plural = 'Record - Range Inspections'

    rangeTestName = models.ForeignKey('rangeTestByPart',verbose_name='Inspection Name')
    jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='ri_jobID')
    machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
                                        related_name='ri_machineOperator')
    inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
                                      related_name='ri_inspectorName')
    dateCreated = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    isFullShot = models.BooleanField(verbose_name="Is Full Shot? (check if true)",default=True)
    headCavID = models.ForeignKey('molds.PartIdentifier', verbose_name="Head and Cavity ID", blank=True, null=True)
    numVal = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Test Value")

    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)


#######################################################################################################################
#
#
# Text Record
#
#
#######################################################################################################################

class textRecord(models.Model):
    class Meta:
        verbose_name = 'Name - Text type Inspection'
        verbose_name_plural = 'Name - Text type Inspection'

    testName = models.CharField(max_length=75, verbose_name="Text Box Inspection Name",unique=True)
    requireAll = models.BooleanField(verbose_name="Require all parts get inspection?",default=False)

    def __unicode__(self):
        return '%s' % (self.testName)

class textRecordByPart(models.Model):
    class Meta:
        verbose_name = 'Part Assignment - Text Test'
        verbose_name_plural = 'Part Assignment - Text Test'
        unique_together = ("testName", "item_Number")

    testName = models.ForeignKey('textRecord', verbose_name = "Text Test Name")
    item_Number = models.ForeignKey('part.Part', verbose_name = "Part Number")

    def __unicode__(self):
        return '%s' % (self.testName)

class textInspection(models.Model):
    class Meta:
        verbose_name = 'Record - Inspection'
        verbose_name_plural = 'Record - Text Inspections'

    textTestName = models.ForeignKey('textRecord',verbose_name='Inspection Name')
    jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='ti_jobID')
    machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
                                        related_name='ti_machineOperator')
    inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
                                      related_name='ti_inspectorName')
    dateCreated = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    isFullShot = models.BooleanField(verbose_name="Is Full Shot? (check if true)",default=True)
    headCavID = models.ForeignKey('molds.PartIdentifier', verbose_name="Head and Cavity ID", blank=True, null=True)
    inspectionResult = models.CharField(verbose_name="Enter Inspection Information:",max_length=75)

    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)