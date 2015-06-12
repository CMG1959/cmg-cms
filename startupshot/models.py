from django.db import models

# Create your models here.

class CIMC_Part(models.Model):
	item_Number = models.CharField(max_length=15)
	item_Description = models.CharField(max_length=75)
	visual_inspection = models.BooleanField(default=True)
	weight_inspection = models.BooleanField(default=True)
	def __unicode__(self):
		return self.item_Number

class CIMC_Production(models.Model):
	item = models.ForeignKey(CIMC_Part)
	jobNumber = models.CharField(max_length=15)
	partWeight = models.DecimalField(max_digits=12,decimal_places=3)
	cavityID = models.CharField(max_length=5)
	headID = models.CharField(max_length=5)
	activeCavities = models.IntegerField()
	dateCreated = models.DateTimeField('date published')
	inProduction = models.BooleanField(default=True)
	machNo = models.CharField(max_length=6)

	def __unicode__(self):
		return self.jobNumber
