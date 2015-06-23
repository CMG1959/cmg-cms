from django.db import models

# Create your models here.
class Part(models.Model):
    # Stuff from TMM will go here
    item_Number = models.CharField(max_length=15)
    item_Description = models.CharField(max_length=75)

    def __unicode__(self):
        return self.item_Number


class PartInspection(models.Model):
    item_Number = models.ForeignKey(Part)
    visual_inspection = models.BooleanField(default=True)
    weight_inspection = models.BooleanField(default=True)
