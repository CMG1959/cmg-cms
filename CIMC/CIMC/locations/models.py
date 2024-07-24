from django.db import models

# Create your models here.
class locations(models.Model):
    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    loc_ID = models.SmallIntegerField()
    loc_Description = models.CharField(max_length=50)
    loc_Country = models.CharField(max_length=2)
    loc_Address_1 = models.CharField(max_length=50)
    loc_Address_2 = models.CharField(max_length=50)
    loc_City = models.CharField(max_length=50)
    loc_ST = models.CharField(max_length=2)
    loc_Zip = models.CharField(max_length=12)

    def __unicode__(self):
        return '%s' % self.loc_Description
