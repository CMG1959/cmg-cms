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
        verbose_name = 'Pass Fail Test Name'
        verbose_name_plural = 'Pass Fail Test Names'

    testName = models.CharField(max_length=25, verbose_name="Pass Fail Test Name",unique=True)

    def __unicode__(self):
        return '%s' % (self.testName)

class passFailTestCriteria(models.Model):
    class Meta:
        verbose_name = 'Pass Fail Test Criteria'
        verbose_name_plural = 'Pass Fail Test Criteria'
        unique_together = ("testName", "passFail")

    testName = models.ForeignKey('passFailTest', verbose_name = "Pass Fail Test Name")
    passFail = models.CharField(max_length=25, verbose_name = "Pass Fail Reason")

    def __unicode__(self):
        return '%s' % (self.passFail)

class passFailByPart(models.Model):
    class Meta:
        verbose_name = 'Pass Fail Test By Part'
        verbose_name_plural = 'Pass Fail By Parts'
        unique_together = ("testName", "item_Number")


    testName = models.ForeignKey('passFailTest', verbose_name = "Pass Fail Test Name")
    item_Number = models.ForeignKey('part.Part', verbose_name = "Part Number")

    def __unicode__(self):
        return '%s - %s' % (self.testName, self.item_Number)

class passFailInspection(models.Model):
    class Meta:
        verbose_name = 'Pass Fail Inspection'
        verbose_name_plural = 'Pass Fail Inspections'

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
        verbose_name = 'Range Test Name'
        verbose_name_plural = 'Range Test Names'

    testName = models.CharField(max_length=25, verbose_name="Range Test Name",unique=True)

    def __unicode__(self):
        return '%s' % (self.testName)

class rangeTestByPart(models.Model):
    class Meta:
        verbose_name = 'Range Test Parameters By Part'
        verbose_name_plural = 'Range Test Parameters By Parts'
        unique_together = ("testName", "item_Number")

    testName = models.ForeignKey('rangeTest', verbose_name = "Range Test Name")
    item_Number = models.ForeignKey('part.Part', verbose_name = "Part Number")
    rangeMin = models.DecimalField(verbose_name="Minimum Value", default=0, max_digits=12,decimal_places=3)
    rangeMax = models.DecimalField(verbose_name="Maximum Value", default=9999999, max_digits=12,decimal_places=3)

    def __unicode__(self):
        return '%s' % (self.testName)

class rangeInspection(models.Model):
    class Meta:
        verbose_name = 'Range Inspection'
        verbose_name_plural = 'Range Inspections'

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



#
# #######################################################################################################################
# #
# #
# # Part Weight Inspection
# #
# #
# #######################################################################################################################
#
# class partWeightInspection(models.Model):
#     class Meta:
#         verbose_name = 'Part Weight Inspection'
#         verbose_name_plural = 'Part Weight Inspections'
#
#     jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='pwi_jobID')
#     machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
#                                         related_name='pwi_machineOperator')
#     inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
#                                       related_name='pwi_inspectorName')
#     dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
#     headCavID = models.ForeignKey('molds.PartIdentifier', verbose_name="Head and Cavity ID")
#     partWeight = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Part Weight")
#
#     def __unicode__(self):
#         return '%s - %s' % (self.jobID, self.dateCreated)
#
# #######################################################################################################################
# #
# #
# # Shot Weight Inspection
# #
# #
# #######################################################################################################################
#
#
# class shotWeightInspection(models.Model):
#     class Meta:
#         verbose_name = 'Shot Weight Inspection'
#         verbose_name_plural = 'Shot Weight Inspections'
#
#     jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='swi_jobID')
#     machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
#                                         related_name='swi_machineOperator')
#     inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
#                                       related_name='swi_inspectorName')
#     dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
#     shotWeight = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Shot Weight")
#     activeCavities = models.IntegerField(verbose_name='Active Cavities',default=1)
#     def __unicode__(self):
#         return '%s - %s' % (self.jobID, self.dateCreated)
#
# #######################################################################################################################
# #
# #
# # Visual Inspection
# #
# #
# #######################################################################################################################
#
# class visualInspectionCriteria(models.Model):
#     class Meta:
#         verbose_name = 'Visual Inspection Criterion'
#         verbose_name_plural = 'Visual Inspection Criteria'
#
#     defectType = models.CharField(max_length=25)
#
#     def __unicode__(self):
#         return self.defectType
#
# class visualInspection(models.Model):
#     class Meta:
#         verbose_name = 'Visual Inspection'
#         verbose_name_plural = 'Visual Inspections'
#
#     jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='vi_jobID')
#     machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
#                                         related_name='vi_machineOperator')
#     inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
#                                       related_name='vi_inspectorName')
#     dateCreated = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
#     inspectionResult = models.BooleanField(verbose_name="Inspection Result (check if passed)",default=True)
#     defectType = models.ManyToManyField(visualInspectionCriteria, verbose_name="Defect Type",blank=True)
#     headCavID = models.ForeignKey('molds.PartIdentifier', verbose_name="Head and Cavity ID")
#
#     def __unicode__(self):
#         return '%s - %s' % (self.jobID, self.dateCreated)
#
# #######################################################################################################################
# #
# #
# # Outside Diameter Inspection
# #
# #
# #######################################################################################################################
#
#
# class outsideDiameterInspection(models.Model):
#     class Meta:
#         verbose_name = 'Outside Diameter Inspection'
#         verbose_name_plural = 'Outside Diameter Inspections'
#
#     jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='odi_jobID')
#     machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
#                                         related_name='odi_machineOperator')
#     inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
#                                       related_name='odi_inspectorName')
#     dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
#     outsideDiameter = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Outside Diameter")
#
#     def __unicode__(self):
#         return '%s - %s' % (self.jobID, self.dateCreated)
#
# #######################################################################################################################
# #
# #
# # Volume Inspection
# #
# #
# #######################################################################################################################
#
# class volumeInspection(models.Model):
#     class Meta:
#         verbose_name = 'Volume Inspection'
#         verbose_name_plural = 'Volume Inspections'
#
#     jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='vol_jobID')
#     machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
#                                         related_name='vol_machineOperator')
#     inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
#                                       related_name='vol_inspectorName')
#     dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
#     liquidWeight = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Liquid Weight (g)")
#
#     def __unicode__(self):
#         return '%s - %s' % (self.jobID, self.dateCreated)
#
# #######################################################################################################################
# #
# #
# # Neck Diameter Inspection
# #
# #
# #######################################################################################################################
#
#
# class neckDiameterInspection(models.Model):
#     class Meta:
#         verbose_name = 'Neck Diameter Inspection'
#         verbose_name_plural = 'Neck Diameter Inspections'
#
#     jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='ndi_jobID')
#     machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
#                                         related_name='ndi_machineOperator')
#     inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
#                                       related_name='ndi_inspectorName')
#     dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
#     testResult = models.BooleanField(verbose_name="Test Result", default=True)
#
#     def __unicode__(self):
#         return '%s - %s' % (self.jobID, self.dateCreated)
#
# #######################################################################################################################
# #
# #
# # Assembly Inspection
# #
# #
# #######################################################################################################################
#
#
# class assemblyTestCriteria(models.Model):
#     class Meta:
#         verbose_name = 'Assembly Test Criteria'
#         verbose_name_plural = 'Assembly Test Criteria'
#
#     assemblyTest = models.CharField(max_length=25, verbose_name="Test type")
#
#     def __unicode__(self):
#         return self.assemblyTest
#
#
# class assemblyTest(models.Model):
#     class Meta:
#         verbose_name = 'Assembly Test Criteria by Model'
#         verbose_name_plural = 'Assembly Test Criteria by Model'
#
#     part = models.ForeignKey('part.Part')
#     assemblyTestItem = models.ForeignKey(assemblyTestCriteria)
#
#     def __unicode__(self):
#         return self.assemblyTestItem.assemblyTest
#
# class assemblyInspection(models.Model):
#     class Meta:
#         verbose_name = 'Assembly Inspection'
#         verbose_name_plural = 'Assembly Inspections'
#
#     jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='assem_jobID')
#     machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
#                                         related_name='assem_machineOperator')
#     inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
#                                       related_name='assem_inspectorName')
#     dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
#     inspectionResult = models.BooleanField(verbose_name="Inspection Result (check if passed)",default=True)
#     assemblyTestResults = models.ManyToManyField(assemblyTest, verbose_name="Assembly Test Results",blank=True)
#
#     def __unicode__(self):
#         return '%s - %s' % (self.jobID, self.dateCreated)
# #######################################################################################################################
# #
# #
# # Carton Temperature
# #
# #
# #######################################################################################################################
#
#
# class cartonTemperature(models.Model):
#     class Meta:
#         verbose_name = 'Carton Temperature'
#         verbose_name_plural = 'Carton Temperatures'
#
#     jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='ct_jobID')
#     machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
#                                         related_name='ct_machineOperator')
#     inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
#                                       related_name='ct_inspectorName')
#     dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
#     cartonTemp = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Carton Temp (F)")
#
#     def __unicode__(self):
#         return '%s - %s' % (self.jobID, self.dateCreated)
#
# #######################################################################################################################
# #
# #
# # Vision System
# #
# #
# #######################################################################################################################
#
#
# class visionTestCriteria(models.Model):
#     class Meta:
#         verbose_name = 'Vision Test Criteria'
#         verbose_name_plural = 'Vision Test Criteria'
#
#     visionTest = models.CharField(max_length=25, verbose_name="Test type")
#
#     def __unicode__(self):
#         return self.visionTest
#
# class visionTest(models.Model):
#     class Meta:
#         verbose_name = 'Vision Test Criteria by Model'
#         verbose_name_plural = 'Vision Test Criteria by Model'
#
#     equipmentID = models.ForeignKey('equipment.EquipmentInfo')
#     visionTestItem = models.ForeignKey(visionTestCriteria)
#
#     def __unicode__(self):
#         return self.assemblyTestItem.assemblyTest
#
#
# class visionInspection(models.Model):
#     class Meta:
#         verbose_name = 'Vision System Test'
#         verbose_name_plural = 'Vision System Test'
#
#     jobID = models.ForeignKey('startupshot.startUpShot', verbose_name="Job ID", related_name='vis_jobID')
#     machineOperator = models.ForeignKey('employee.Employees', verbose_name="Machine Operator",
#                                         related_name='vis_machineOperator')
#     inspectorName = models.ForeignKey('employee.Employees', verbose_name="Inspector Name",
#                                       related_name='vis_inspectorName')
#     dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
#     inspectionResult = models.BooleanField(verbose_name="Inspection Result (check if passed)",default=True)
#     visionTestResults = models.ManyToManyField(visionTest, verbose_name="Vision System Test Results",blank=True)
#
#     def __unicode__(self):
#         return '%s - %s' % (self.jobID, self.dateCreated)
#
