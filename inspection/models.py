from datetime import datetime
from django.db import models

# Create your models here.

class visualInspectionCriteria(models.Model):
	defectType = models.CharField(max_length=25)
	def __unicode__(self):
		return self.defectType


class partWeightInspection(models.Model):
	jobID = models.ForeignKey('startupshot.Production', verbose_name="Job ID", related_name='pwi_jobID')
	machineOperator = models.ForeignKey('employee.employee', verbose_name="Machine Operator",related_name='pwi_machineOperator')
	inspectorName = models.ForeignKey('employee.employee', verbose_name="Inspector Name",related_name='pwi_inspectorName')
	dateCreated = models.DateTimeField(verbose_name="Date Created",auto_now_add=True)
	headCavID = models.ForeignKey('molds.PartIdentifier', verbose_name="Head and Cavity ID")
	partWeight = models.DecimalField(max_digits=12,decimal_places=3, verbose_name="Part Weight")


class visualInspection(models.Model):
	jobID = models.ForeignKey('startupshot.Production',  verbose_name="Job ID",related_name='vi_jobID')
	machineOperator = models.ForeignKey('employee.employee', verbose_name="Machine Operator",related_name='vi_machineOperator')
	inspectorName = models.ForeignKey('employee.employee', verbose_name="Inspector Name",related_name='vi_inspectorName')
	dateCreated = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
	inspectionResult = models.BooleanField( verbose_name="Inspection Result")
	defectType = models.ManyToManyField(visualInspectionCriteria, verbose_name="Defect Type")
	headCavID = models.ForeignKey('molds.PartIdentifier', verbose_name="Head and Cavity ID")
