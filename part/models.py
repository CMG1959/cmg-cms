from django.db import models

# Create your models here.
class Part(models.Model):
    # Stuff from TMM will go here
    class Meta:
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'

    item_Number = models.CharField(verbose_name="Item Number", max_length=15)
    item_Description = models.CharField(verbose_name="Item Description", max_length=75)
    exp_part_weight = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Expected Part Weight")
    exp_cycle_time = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Expected Cycle Time")

    def __unicode__(self):
        return self.item_Number


class PartInspection(models.Model):
    class Meta:
        verbose_name = 'Required Part Inspection'
        verbose_name_plural = 'Required Part Inspections'

    item_Number = models.ForeignKey(Part, verbose_name="Item Number")
    visual_inspection = models.BooleanField(verbose_name="Visual Inspection", default=True)
    part_weight_inspection = models.BooleanField(verbose_name="Part Weight Inspection", default=False)
    shot_weight_inspection = models.BooleanField(verbose_name="Shot Weight Inspection", default=True)

    def __unicode__(self):
        return '%s' % (self.item_Number)
