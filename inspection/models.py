from datetime import datetime
from django.db import models

# Create your models here.

class visualInspectionCriteria(models.Model):
	defectType = models.CharField(max_length=25)
	def __unicode__(self):
		return self.defectType


class partWeightInspection(models.Model):
	jobID = models.ForeignKey('startupshot.Production', related_name='pwi_jobID')
	machineOperator = models.ForeignKey('employee.employee',related_name='pwi_machineOperator')
	inspectorName = models.ForeignKey('employee.employee',related_name='pwi_inspectorName')
	dateCreated = models.DateTimeField('date published',default=datetime.now)
	headCavID = models.ForeignKey('molds.PartIdentifier')
	partWeight = models.DecimalField(max_digits=12,decimal_places=3)


class visualInspection(models.Model):
	jobID = models.ForeignKey('startupshot.Production', related_name='vi_jobID')
	machineOperator = models.ForeignKey('employee.employee',related_name='vi_machineOperator')
	inspectorName = models.ForeignKey('employee.employee',related_name='vi_inspectorName')
	dateCreated = models.DateTimeField('date published',default=datetime.now)
	inspectionResult = models.BooleanField()
	defectType = models.ManyToManyField(visualInspectionCriteria)
	headCavID = models.ForeignKey('molds.PartIdentifier')
