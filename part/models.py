from django.db import models

#######################################################################################################################
#
#
# TMM Part Info
#
#
#######################################################################################################################

# Create your models here.
class Part(models.Model):
    # Stuff from TMM will go here
    class Meta:
        verbose_name = 'TMM Part'
        verbose_name_plural = 'TMM Parts'
        ordering = ('item_Number',)


    item_Number = models.CharField(verbose_name="Item Number", max_length=15)
    item_Description = models.CharField(verbose_name="Item Description", max_length=75)
    exp_part_weight = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Expected Part Weight")
    exp_cycle_time = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Expected Cycle Time")



    def __unicode__(self):
        return self.item_Number

#######################################################################################################################
#
#
# Part Inspection Types
#
#
#######################################################################################################################


class PartInspection(models.Model):
    class Meta:
        verbose_name = 'Required Part Inspection'
        verbose_name_plural = 'Required Part Inspections'
        ordering = ('item_Number')

    ### Item Info
    item_Number = models.ForeignKey(Part, verbose_name="Item Number")
    ### Inspection Types
    ## Pass/Fail with select
    visual_inspection = models.BooleanField(verbose_name="Visual Inspection", default=True)
    assembly_test_inspection = models.BooleanField(verbose_name="Assembly Test Inspection", default=False)
    vision_system_inspection = models.BooleanField(verbose_name="Vision System", default=False)
    ## Min/Max inspection
    part_weight_inspection = models.BooleanField(verbose_name="Part Weight Inspection", default=False)
    shot_weight_inspection = models.BooleanField(verbose_name="Shot Weight Inspection", default=True)
    od_inspection = models.BooleanField(verbose_name="Outside Diameter Inspection", default=False)
    vol_inspection = models.BooleanField(verbose_name="Volume Inspection", default=False)
    neck_diameter_inspection = models.BooleanField(verbose_name="Neck Diameter Inspection", default=False)
    carton_temp_inspection = models.BooleanField(verbose_name="Carton Temperature", default=False)
    ## Min/Max Parameters
    min_part_weight = models.DecimalField(verbose_name="Minimum Part Weight", default=0, max_digits=12,decimal_places=3)
    max_part_weight = models.DecimalField(verbose_name="Maximum Part Weight", default=999999999, max_digits=12,decimal_places=3)
    min_od = models.DecimalField(verbose_name="Minimum Outside Diameter", default=0, max_digits=12,decimal_places=3)
    max_od = models.DecimalField(verbose_name="Maximum Outside Diameter", default=999999999, max_digits=12,decimal_places=3)
    min_vol = models.DecimalField(verbose_name="Minimum Volume", default=0, max_digits=12,decimal_places=3)
    max_vol = models.DecimalField(verbose_name="Maximum Volume", default=999999999, max_digits=12,decimal_places=3)
    min_neck_diam = models.DecimalField(verbose_name="Minimum Neck Diameter", default=0, max_digits=12,decimal_places=3)
    max_neck_diam = models.DecimalField(verbose_name="Maximum Neck Diameter", default=999999999, max_digits=12,decimal_places=3)
    min_carton_temp = models.DecimalField(verbose_name="Minimum Carton Temp", default=0, max_digits=12,decimal_places=3)
    min_carton_tempt = models.DecimalField(verbose_name="Maximum Carton Temp", default=999999999, max_digits=12,decimal_places=3)
    def __unicode__(self):
        return '%s' % (self.item_Number)

