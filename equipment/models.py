from django.db import models
from datetime import date
# Create your models here.
class EquipmentType(models.Model):
    equipment_type = models.CharField(max_length=50)  # Robot, IMM, ISBM

    def __unicode__(self):
        return self.equipment_type


class EquipmentManufacturer(models.Model):
    manufacturer_name = models.CharField(max_length=50)  # e.g. Wittmann

    def __unicode__(self):
        return self.manufacturer_name


class EquipmentInfo(models.Model):
    equipment_type = models.ForeignKey(EquipmentType)
    part_identifier = models.CharField(max_length=25)  # common name like IMM02
    manufacturer_name = models.ForeignKey(EquipmentManufacturer)
    serial_number = models.CharField(max_length=25)
    date_of_manufacture = models.DateField(default=date.today)

    def __unicode__(self):
        return self.part_identifier
