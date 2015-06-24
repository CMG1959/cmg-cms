from django.db import models
from datetime import date
# Create your models here.
class EquipmentType(models.Model):
    equipment_type = models.CharField( verbose_name="Equipment Type",max_length=50)  # Robot, IMM, ISBM

    def __unicode__(self):
        return self.equipment_type


class EquipmentManufacturer(models.Model):
    manufacturer_name = models.CharField( verbose_name="Manufacturer Name",max_length=50)  # e.g. Wittmann

    def __unicode__(self):
        return self.manufacturer_name


class EquipmentInfo(models.Model):
    equipment_type = models.ForeignKey(EquipmentType, verbose_name="Equipment Type")
    part_identifier = models.CharField( verbose_name="Identifier",max_length=25)  # common name like IMM02
    manufacturer_name = models.ForeignKey(EquipmentManufacturer, verbose_name="Manufacturer Name")
    serial_number = models.CharField( verbose_name="Serial Number",max_length=25)
    date_of_manufacture = models.DateField( verbose_name="Date of Manufacture",default=date.today)

    def __unicode__(self):
        return self.part_identifier
