from django.db import models
from django.conf import settings
# Create your models here.

class Mold(models.Model):
    # Will come from TMM
    class Meta:
        verbose_name = 'TMM Mold Information'
        verbose_name_plural = 'TMM Mold Information'
        ordering = ('mold_number',)

    mold_number = models.CharField(verbose_name="Mold Number", max_length=20)
    mold_description = models.CharField(verbose_name="Mold Description", max_length=50)
    num_cavities = models.IntegerField(verbose_name="Number of Cavities")
    loc_id = models.SmallIntegerField(verbose_name="Location ID",default=int(settings.PLANT_LOC))

    def __unicode__(self):
        return self.mold_number


class PartIdentifier(models.Model):
    # Will be filled in by script
    mold_number = models.ForeignKey(Mold, verbose_name="Mold Number")
    head_code = models.CharField(max_length=5, verbose_name="Head Code")
    cavity_id = models.CharField(max_length=5, verbose_name="Cavity ID")

    def __unicode__(self):
        return '%s - %s' % (self.head_code, self.cavity_id)
