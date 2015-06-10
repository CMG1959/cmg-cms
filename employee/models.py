from django.db import models

# Create your models here.

class cimc_organizations(models.Model):
	org_name = models.CharField(max_length=25)

	def __unicode__(self):
		return self.org_name

class employee(models.Model):
	last_name = models.CharField(max_length=25)
	first_name = models.CharField(max_length=25)
	employee_id = models.CharField(max_length=25)
	organization_name = models.ForeignKey(cimc_organizations)

	def __unicode__(self):
		return '%s - %s' % (self.last_name,self.first_name)