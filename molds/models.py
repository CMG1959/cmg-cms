from django.db import models

# Create your models here.

class Mold(models.Model):
    mold_number = models.CharField(max_length=15)
    mold_description = models.CharField(max_length=30)
    num_cavities = models.IntegerField()

    def __unicode__(self):
        return self.mold_number


class PartIdentifier(models.Model):
    mold_number = models.ForeignKey(Mold)
    head_code = models.CharField(max_length=5)
    cavity_id = models.CharField(max_length=5)

    def __unicode__(self):
        return '%s - %s' % (self.head_code, self.cavity_id)
