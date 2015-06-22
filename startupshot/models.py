from django.db import models
# from molds.models import Mold, PartIdentifier
# Create your models here.

# class CIMC_Part(models.Model):
# 	item_Number = models.CharField(max_length=15)
# 	item_Description = models.CharField(max_length=75)
# 	visual_inspection = models.BooleanField(default=True)
# 	weight_inspection = models.BooleanField(default=True)
# 	def __unicode__(self):
# 		return self.item_Number

class Production(models.Model):
	item = models.ForeignKey('part.Part')
	jobNumber = models.CharField(max_length=15)
	moldNumber = models.ForeignKey('molds.Mold')
	headCavID = models.ForeignKey('molds.PartIdentifier')
	partWeight = models.DecimalField(max_digits=12,decimal_places=3)
	activeCavities = models.IntegerField()
	dateCreated = models.DateTimeField('date published')
	inProduction = models.BooleanField(default=True)
	machNo = models.ForeignKey('equipment.EquipmentInfo')

	def __unicode__(self):
		return self.jobNumber
