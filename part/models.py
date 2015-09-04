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
        return '%s' % (self.item_Number)



    def __unicode__(self):
        return self.item_Number
