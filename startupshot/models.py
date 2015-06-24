from django.db import models
# from molds.models import Mold, PartIdentifier
# Create your models here.



class Production(models.Model):
	item = models.ForeignKey('part.Part')
	jobNumber = models.CharField(max_length=15, unique=True)
	moldNumber = models.ForeignKey('molds.Mold')
	# headCavID = models.ForeignKey('molds.PartIdentifier')
	# partWeight = models.DecimalField(max_digits=12,decimal_places=3)
	activeCavities = models.IntegerField()
	dateCreated = models.DateTimeField(auto_now_add=True)
	machNo = models.ForeignKey('equipment.EquipmentInfo')
	inspectorName = models.ForeignKey('employee.employee')
	shotWeight = models.DecimalField(max_digits=12,decimal_places=3)

	def __unicode__(self):
		return self.jobNumber


class MattecProd(models.Model):
	### This information will be taken from MATTEC via SQL script
	jobNumber = models.CharField(max_length=15)
	machNo = models.CharField(max_length=10)
	itemDesc = models.CharField(max_length=50)
	itemNo = models.CharField(max_length=15)
	moldNumber = models.CharField(max_length=15)
	activeCavities = models.IntegerField()

	def __unicode__(self):
		return '%s - %s' % (self.machNo,self.itemDesc)