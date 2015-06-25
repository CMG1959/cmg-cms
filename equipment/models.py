from django.db import models
from datetime import date
# Create your models here.
class EquipmentType(models.Model):
    class Meta:
        verbose_name='Equipment Type'
        verbose_name_plural='Equipment Types'

    equipment_type = models.CharField( verbose_name="Equipment Type",max_length=50)  # Robot, IMM, ISBM

    def __unicode__(self):
        return self.equipment_type


class EquipmentManufacturer(models.Model):
    class Meta:
        verbose_name='Equipment Manufacturer'
        verbose_name_plural='Equipment Manufacturers'

    manufacturer_name = models.CharField( verbose_name="Manufacturer Name",max_length=50)  # e.g. Wittmann

    def __unicode__(self):
        return self.manufacturer_name


class EquipmentInfo(models.Model):
    class Meta:
        verbose_name='Equipment Information'
        verbose_name_plural='Equipment Information'

    equipment_type = models.ForeignKey(EquipmentType, verbose_name="Equipment Type")
    part_identifier = models.CharField( verbose_name="Identifier",max_length=25)  # common name like IMM02
    manufacturer_name = models.ForeignKey(EquipmentManufacturer, verbose_name="Manufacturer Name")
    serial_number = models.CharField( verbose_name="Serial Number",max_length=25)
    date_of_manufacture = models.DateField( verbose_name="Date of Manufacture",default=date.today)

    def __unicode__(self):
        return self.part_identifier


class PMFreq(models.Model):
    class Meta:
        verbose_name='Preventative Maintenance Frequency'
        verbose_name_plural='Preventative Maintenance Frequencies'

    # Month, Quarterly, Weekly, Yearly
    pm_frequency = models.CharField(verbose_name="PM Frequency", max_length=25)

    def __unicode__(self):
        return self.pm_frequency


class PM(models.Model):
    class Meta:
        verbose_name = 'Preventative Maintenance Item'
        verbose_name_plural = 'Preventative Maintenance Items'

    # This is for adding PM information such as grease, inspect, etc
    equipment_type = models.ForeignKey('EquipmentType', verbose_name='Equipment Type')
    pm_frequency = models.ForeignKey('PMFreq',verbose_name='PM Frequency')
    pm_item = models.CharField(max_length=50)
    def __unicode__(self):
        return self.pm_item


class EquipmentPM(models.Model):
    class Meta:
        verbose_name = 'Perform PM'
        verbose_name_plural = 'Performed PM'

    employee = models.ForeignKey('employee.employee', verbose_name="Technician")
    dateCreated = models.DateTimeField(verbose_name="Date Created",auto_now_add=True)
    pm_frequency = models.ForeignKey('PMFreq', verbose_name="PM Frequency")
    equipment_ID = models.ForeignKey('EquipmentInfo', verbose_name="Equipment ID")
    logged_pm = models.ManyToManyField('PM', verbose_name="PM Items")


