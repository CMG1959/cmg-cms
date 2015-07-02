from django.db import models

# Create your models here.

class Mold(models.Model):
    class Meta:
        verbose_name = 'Mold Information'
        verbose_name_plural = 'Molds Information'

    mold_number = models.CharField(verbose_name="Mold Number", max_length=15)
    mold_description = models.CharField(verbose_name="Mold Description", max_length=30)
    num_cavities = models.IntegerField(verbose_name="Number of Cavities")

    def __unicode__(self):
        return self.mold_number


class PartIdentifier(models.Model):
    mold_number = models.ForeignKey(Mold, verbose_name="Mold Number")
    head_code = models.CharField(max_length=5, verbose_name="Head Code")
    cavity_id = models.CharField(max_length=5, verbose_name="Cavity ID")

    def __unicode__(self):
        return '%s - %s' % (self.head_code, self.cavity_id)
