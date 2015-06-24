from django.db import models

# Create your models here.
class Part(models.Model):
    # Stuff from TMM will go here
    item_Number = models.CharField( verbose_name="Item Number",max_length=15)
    item_Description = models.CharField( verbose_name="Item Description",max_length=75)

    def __unicode__(self):
        return self.item_Number


class PartInspection(models.Model):
    item_Number = models.ForeignKey(Part, verbose_name="Item Number")
    visual_inspection = models.BooleanField( verbose_name="Visual Inspection",default=True)
    weight_inspection = models.BooleanField( verbose_name="Weight Inspection",default=True)
