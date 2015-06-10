from datetime import datetime
from django.db import models

# Create your models here.

class visualInspectionCriteria(models.Model):
	defectType = models.CharField(max_length=25)
	def __unicode__(self):
		return self.defectType


class partWeightInspection(models.Model):
	jobID = models.ForeignKey('startupshot.CIMC_Production')
	machineOperator = models.ForeignKey('employee.employee',related_name='machineOperator')
	inspectorName = models.ForeignKey('employee.employee',related_name='inspectorName')
	dateCreated = models.DateTimeField('date published',default=datetime.now)
	cavityID = models.CharField(max_length=5)
	partWeight = models.DecimalField(max_digits=12,decimal_places=3)


class visualInspection(models.Model):
	jobID = models.ForeignKey('startupshot.CIMC_Production')
	machineOperator = models.ForeignKey('employee.employee',related_name='machineOperator')
	inspectorName = models.ForeignKey('employee.employee',related_name='inspectorName')
	dateCreated = models.DateTimeField('date published',default=datetime.now)
	inspectionResult = models.BooleanField()
	defectType = models.ManyToManyField(visualInspectionCriteria)
	cavityID = models.CharField(max_length=5)
	partWeight = models.DecimalField(max_digits=12,decimal_places=3)