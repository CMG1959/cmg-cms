from datetime import date
from django.db import models


class EquipmentClass(models.Model):
    class Meta:
        verbose_name = 'Equipment - Class'
        verbose_name_plural = 'Equipment - Class'

    group_name = models.CharField(verbose_name='Group Name', max_length=50, unique=True)

    def __unicode__(self):
        return self.group_name

# Create your models here.
class EquipmentType(models.Model):
    class Meta:
        verbose_name = 'Equipment - Type'
        verbose_name_plural = 'Equipment - Types'

    equipment_type = models.CharField(verbose_name="Equipment Type", max_length=50, unique=True)  # Robot, IMM, ISBM
    equipment_class = models.ForeignKey(EquipmentClass, verbose_name="Equipment Class")
    tooltip_content = models.CharField(verbose_name= "Tooltip", max_length=256, null=True, default="")

    def __unicode__(self):
        return self.equipment_type



class EquipmentManufacturer(models.Model):
    class Meta:
        verbose_name = 'Equipment - Manufacturer'
        verbose_name_plural = 'Equipment - Manufacturers'

    manufacturer_name = models.CharField(verbose_name="Manufacturer Name", max_length=50, unique=True)  # e.g. Wittmann

    def __unicode__(self):
        return self.manufacturer_name


class EquipmentInfo(models.Model):
    class Meta:
        verbose_name = 'Equipment - Information'
        verbose_name_plural = 'Equipment - Information'

    equipment_type = models.ForeignKey(EquipmentType, verbose_name="Equipment Type")
    part_identifier = models.CharField(verbose_name="Machine ID (alias)", max_length=25)
    manufacturer_name = models.ForeignKey(EquipmentManufacturer, verbose_name="Manufacturer Name")
    serial_number = models.CharField(verbose_name="Serial Number", max_length=25)
    date_of_manufacture = models.DateField(verbose_name="Date of Manufacture", default=date.today)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)

    def __unicode__(self):
        return self.part_identifier


class PMFreq(models.Model):
    class Meta:
        verbose_name = 'Equipment - Preventative Maintenance Frequency'
        verbose_name_plural = 'Equipment - Preventative Maintenance Frequencies'

    # Month, Quarterly, Weekly, Yearly
    pm_frequency = models.CharField(verbose_name="PM Frequency", max_length=25)

    def __unicode__(self):
        return self.pm_frequency


class PM(models.Model):
    class Meta:
        verbose_name = 'Equipment - Preventative Maintenance Item'
        verbose_name_plural = 'Equipment - Preventative Maintenance Items'

    # This is for adding PM information such as grease, inspect, etc
    equipment_type = models.ForeignKey('EquipmentType', verbose_name='Equipment Type')
    pm_frequency = models.ForeignKey('PMFreq', verbose_name='PM Frequency')
    pm_item = models.CharField(max_length=50)

    def __unicode__(self):
        return self.pm_item


class EquipmentPM(models.Model):
    class Meta:
        verbose_name = 'Record - Performed PM'
        verbose_name_plural = 'Record - Performed PM'

    Date_Performed = models.DateField(verbose_name='Date Performed', default=date.today)
    employee = models.ForeignKey('employee.Employees', verbose_name="Technician", blank=True)
    dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    pm_frequency = models.ForeignKey('PMFreq', verbose_name="PM Frequency")
    equipment_ID = models.ForeignKey('EquipmentInfo', verbose_name="Equipment ID")
    logged_pm = models.ManyToManyField('PM', verbose_name="PM Items")
    comments = models.CharField(max_length=1000, verbose_name="Event Description",null=True,blank=True)


    def __unicode__(self):
        return '%s - %s - %s' % (self.equipment_ID, self.pm_frequency, self.dateCreated)


class EquipmentRepair(models.Model):
    class Meta:
        verbose_name = 'Record - Equipment Repairs'
        verbose_name_plural = 'Record - Equipment Repairs'

    Date_Performed = models.DateField(verbose_name='Date Performed', default=date.today)
    employee = models.ForeignKey('employee.Employees', verbose_name="Technician", blank=True)
    dateCreated = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    equipment_ID = models.ForeignKey('EquipmentInfo', verbose_name="Equipment ID")
    po_num = models.CharField(verbose_name='PO Number', max_length=25, null=True, blank=True)
    part_supplier = models.ForeignKey('supplier.supplier', verbose_name='Part Supplier', null=True, blank=True)
    part_name = models.CharField(verbose_name='Part Name', max_length=50, null=True, blank=True)
    part_number = models.CharField(verbose_name='Part Number', max_length=25, null=True, blank=True)
    part_cost = models.DecimalField(verbose_name='Unit Cost', max_digits=12, decimal_places=2, null=True, blank=True)
    part_quantity = models.IntegerField(verbose_name='Quantity', null=True, blank=True)
    comments = models.CharField(max_length=1000, verbose_name="Event Description", null=True,blank=True)

    def __unicode__(self):
        return '%s - %s - %s' % (self.equipment_ID, self.dateCreated, self.part_name)
