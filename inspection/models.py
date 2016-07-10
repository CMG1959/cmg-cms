from datetime import datetime

from django.db import models
from django.core.validators import RegexValidator
import re
import uuid

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
    isSystemInspection = models.BooleanField(verbose_name="System Inspection?", default=False)
    IsCavity_Instanced = models.BooleanField(verbose_name="Is Cavity Instanced?", default=False)


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
    inspections_per_shift = models.IntegerField(verbose_name = 'Inspections Per Shift',default=2)

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
                                      related_name='pf_inspectorName', blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    inspectionResult = models.BooleanField(verbose_name="Inspection Result (check if passed)",default=True)
    defectType = models.ManyToManyField('passFailTestCriteria', verbose_name="Defect Type",  blank=True)
    headCavID = models.CharField(max_length=8, verbose_name="Cavity Info", null=True, blank=True)
    Passed_Partial = models.BooleanField(verbose_name="Partial Passed?", default=False)
    CavID = models.CharField(max_length=8, verbose_name="Cavity ID", default='-', null=True, blank=True)
    CavGroupID = models.CharField(max_length=8, verbose_name="Cavity Group", default='-', null=True, blank=True)


    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)


#######################################################################################################################
#
#
# Range Inspection
#
#
#######################################################################################################################

class numericTest(models.Model):
    class Meta:
        verbose_name = 'Name - Numeric Test'
        verbose_name_plural = 'Name - Numeric Test'
        db_table = 'inspection_numerictest'

    testName = models.CharField(max_length=75, verbose_name="Range Test Name",unique=True)
    requireAll = models.BooleanField(verbose_name="Require all parts get inspection?",default=False)
    calcAvg = models.BooleanField(verbose_name="Report raw data (do not take average)?",default=False)
    isSystemInspection = models.BooleanField(verbose_name="System Inspection?", default=False)
    hasTimeDelayInspection = models.BooleanField(verbose_name="Inspect Again After Time Period?", default=False)
    IsCavity_Instanced = models.BooleanField(verbose_name="Is Cavity Instanced?", default=False)

    def __unicode__(self):
        return '%s' % (self.testName)

class numericTestByPart(models.Model):
    class Meta:
        verbose_name = 'Part Assignment - Numeric Test Parameters'
        verbose_name_plural = 'Part Assignment - Numeric Test Parameters'
        unique_together = ("testName", "item_Number")
        db_table = 'inspection_numerictestbypart'

    testName = models.ForeignKey('numericTest', verbose_name ="Range Test Name")
    item_Number = models.ForeignKey('part.Part', verbose_name = "Part Number")
    rangeMin = models.DecimalField(verbose_name="Minimum Value", default=0, max_digits=12,decimal_places=3)
    rangeMax = models.DecimalField(verbose_name="Maximum Value", default=9999999, max_digits=12,decimal_places=3)
    inspections_per_shift = models.IntegerField(verbose_name = 'Inspections Per Shift',default=2)
    # systest_link_id = models.UUIDField(max_length=36, blank=True, null=True, default=uuid.uuid4,
    #                                    db_column='SysTest_Link_ID')

    def __unicode__(self):
        return '%s' % (self.testName)

class numericInspection(models.Model):
    class Meta:
        verbose_name = 'Record - Numeric Inspection'
        verbose_name_plural = 'Record - Numeric Inspections'
        db_table = 'inspection_numericinspection'

    numericTestName = models.ForeignKey('numericTestByPart', verbose_name='Inspection Name', db_column='numericTestName_id')
    jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='ri_jobID')
    machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
                                        related_name='ri_machineOperator')
    inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
                                      related_name='ri_inspectorName', blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    isFullShot = models.BooleanField(verbose_name="Is Full Shot? (check if true)",default=True)
    numVal_1 = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Measurement", db_column='numVal_1')
    inspectionResult = models.BooleanField(verbose_name="Inspection Result (check if passed)",default=False)
    timeDelayNumVal = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Measurement after time", blank=True,
                                          null=True)
    headCavID = models.CharField(max_length=8, verbose_name="Cavity Info", null=True, blank=True)
    Passed_Partial = models.BooleanField(verbose_name="Partial Passed?", default=False)

    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)


#######################################################################################################################
#
#
# Small Text Record
#
#
#######################################################################################################################

class textRecord(models.Model):
    class Meta:
        verbose_name = 'Name - Small Text type Inspection'
        verbose_name_plural = 'Name - Small Text type Inspection'

    testName = models.CharField(max_length=75, verbose_name="Text Box Inspection Name",unique=True)
    requireAll = models.BooleanField(verbose_name="Require all parts get inspection?",default=False)
    isSystemInspection = models.BooleanField(verbose_name="System Inspection?", default=False)
    IsCavity_Instanced = models.BooleanField(verbose_name="Is Cavity Instanced?", default=False)

    def __unicode__(self):
        return '%s' % (self.testName)

class textRecordByPart(models.Model):
    class Meta:
        verbose_name = 'Part Assignment - Small Text Test'
        verbose_name_plural = 'Part Assignment - Small Text Test'
        unique_together = ("testName", "item_Number")

    testName = models.ForeignKey('textRecord', verbose_name = "Text Test Name")
    item_Number = models.ForeignKey('part.Part', verbose_name = "Part Number")
    inspections_per_shift = models.IntegerField(verbose_name = 'Inspections Per Shift',default=2)

    def __unicode__(self):
        return '%s' % (self.testName)

class textInspection(models.Model):
    class Meta:
        verbose_name = 'Record - Small Text Inspection'
        verbose_name_plural = 'Record - Small Text Inspections'

    textTestName = models.ForeignKey('textRecord',verbose_name='Inspection Name')
    jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='ti_jobID')
    machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
                                        related_name='ti_machineOperator')
    inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
                                      related_name='ti_inspectorName', blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    isFullShot = models.BooleanField(verbose_name="Is Full Shot? (check if true)",default=True)
    inspectionResult = models.CharField(verbose_name="Enter Inspection Information:",max_length=75)
    headCavID = models.CharField(max_length=8, verbose_name="Cavity Info", null=True, blank=True)
    Passed_Partial = models.BooleanField(verbose_name="Partial Passed?", default=False)


    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)


#######################################################################################################################
#
#
# Integer Record
#
#
#######################################################################################################################

# class IntegerRecord(models.Model):
#     class Meta:
#         verbose_name = 'Name - Integer Type Inspection'
#         verbose_name_plural = 'Name - Integer Type Inspection'
#         db_table = 'inspection_specimenrecord'
#
#     testName = models.CharField(max_length=75, verbose_name="Integer Inspection Name",unique=True)
#     requireAll = models.BooleanField(verbose_name="Require all parts get inspection?",default=False)
#     isSystemInspection = models.BooleanField(verbose_name="System Inspection?", default=False)
#     IsCavity_Instanced = models.BooleanField(verbose_name="Is Cavity Instanced?", default=False)
#
#     def __unicode__(self):
#         return '%s' % (self.testName)
#
# class IntegerRecordByPart(models.Model):
#     class Meta:
#         verbose_name = 'Part Assignment - Integer Type Test'
#         verbose_name_plural = 'Part Assignment - Integer Type Test'
#         unique_together = ("testName", "item_Number")
#         db_table = 'inspection_specimenrecordbypart'
#
#     testName = models.ForeignKey('IntegerRecord', verbose_name = "Integer Test Name")
#     item_Number = models.ForeignKey('part.Part', verbose_name = "Part Number")
#     inspections_per_shift = models.IntegerField(verbose_name = 'Inspections Per Shift',default=2)
#
#     def __unicode__(self):
#         return '%s' % (self.testName)
#
# class IntegerInspection(models.Model):
#     class Meta:
#         verbose_name = 'Record - Integer Inspection'
#         verbose_name_plural = 'Record - Integer Inspections'
#         db_table = 'inspection_specimeninspection'
#
#     integerTestName = models.ForeignKey('IntegerRecord',verbose_name='Inspection Name')
#     jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='Integer_jobID')
#     machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
#                                         related_name='Integer_machineOperator')
#     inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
#                                       related_name='Integer_inspectorName', blank=True)
#     dateCreated = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
#     isFullShot = models.BooleanField(verbose_name="Is Full Shot? (check if true)",default=True)
#     inspectionResult = models.CharField(max_length=38, verbose_name="Enter Inspection Information:")
#     headCavID = models.CharField(max_length=8, verbose_name="Cavity Info", null=True, blank=True)
#     Passed_Partial = models.BooleanField(verbose_name="Partial Passed?", default=False)
#
#     def __unicode__(self):
#         return '%s - %s' % (self.jobID, self.dateCreated)

#######################################################################################################################
#
#
# Float Record
#
#
#######################################################################################################################

class RangeRecord(models.Model):
    class Meta:
        verbose_name = 'Name - Range Type Inspection'
        verbose_name_plural = 'Name - Range Type Inspection'
        db_table = 'inspection_rangerecord'

    testName = models.CharField(max_length=75, verbose_name="Float Inspection Name",unique=True)
    requireAll = models.BooleanField(verbose_name="Require all parts get inspection?",default=False)
    isSystemInspection = models.BooleanField(verbose_name="System Inspection?", default=False)
    IsCavity_Instanced = models.BooleanField(verbose_name="Is Cavity Instanced?", default=False)

    def __unicode__(self):
        return '%s' % (self.testName)

class RangeRecordByPart(models.Model):
    class Meta:
        verbose_name = 'Part Assignment - Range Type Test'
        verbose_name_plural = 'Part Assignment - Range Type Test'
        unique_together = ("testName", "item_Number")
        db_table = 'inspection_rangerecordbypart'

    testName = models.ForeignKey('RangeRecord', verbose_name ="Range Test Name")
    item_Number = models.ForeignKey('part.Part', verbose_name = "Part Number")
    inspections_per_shift = models.IntegerField(verbose_name = 'Inspections Per Shift',default=2)
    rangeMin = models.DecimalField(verbose_name="Minimum Value", default=0, max_digits=12,decimal_places=3)
    rangeMax = models.DecimalField(verbose_name="Maximum Value", default=9999999, max_digits=12,decimal_places=3)

    def __unicode__(self):
        return '%s' % (self.testName)

class RangeInspection(models.Model):
    class Meta:
        verbose_name = 'Record - Range Inspection'
        verbose_name_plural = 'Record - Range Inspections'
        db_table = 'inspection_rangeinspection'

    rangeTestName = models.ForeignKey('RangeRecord', verbose_name='Inspection Name', db_column='rangeTestName_id')
    jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='Float_jobID')
    machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
                                        related_name='float_machineOperator')
    inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
                                      related_name='float_inspectorName', blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    isFullShot = models.BooleanField(verbose_name="Is Full Shot? (check if true)",default=True)
    inspectionResult = models.BooleanField(verbose_name="Inspection Result (check if passed)",default=False)
    numVal_1 = models.DecimalField(verbose_name="Low", max_digits=12, decimal_places=3, db_column='numVal_1')
    numVal_2 = models.DecimalField(verbose_name="High", max_digits=12, decimal_places=3, db_column='numVal_2')
    headCavID = models.CharField(max_length=8, verbose_name="Cavity Info", null=True, blank=True)
    Passed_Partial = models.BooleanField(verbose_name="Partial Passed?", default=False)


    def __unicode__(self):
        return '%s - %s' % (self.jobID, self.dateCreated)