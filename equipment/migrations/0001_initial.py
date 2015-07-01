# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):
    dependencies = [
        ('supplier', '__first__'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('part_identifier', models.CharField(max_length=25, verbose_name=b'Identifier')),
                ('serial_number', models.CharField(max_length=25, verbose_name=b'Serial Number')),
                ('date_of_manufacture',
                 models.DateField(default=datetime.date.today, verbose_name=b'Date of Manufacture')),
            ],
            options={
                'verbose_name': 'Equipment Information',
                'verbose_name_plural': 'Equipment Information',
            },
        ),
        migrations.CreateModel(
            name='EquipmentManufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('manufacturer_name', models.CharField(max_length=50, verbose_name=b'Manufacturer Name')),
            ],
            options={
                'verbose_name': 'Equipment Manufacturer',
                'verbose_name_plural': 'Equipment Manufacturers',
            },
        ),
        migrations.CreateModel(
            name='EquipmentPM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('employee', models.ForeignKey(verbose_name=b'Technician', to='employee.employee')),
                ('equipment_ID', models.ForeignKey(verbose_name=b'Equipment ID', to='equipment.EquipmentInfo')),
            ],
            options={
                'verbose_name': 'Perform PM',
                'verbose_name_plural': 'Performed PM',
            },
        ),
        migrations.CreateModel(
            name='EquipmentRepair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('po_num', models.CharField(max_length=25, verbose_name=b'PO Number')),
                ('part_name', models.CharField(max_length=50, verbose_name=b'Part Name')),
                ('part_number', models.CharField(max_length=25, verbose_name=b'Part Number')),
                ('part_cost', models.DecimalField(verbose_name=b'Unit Cost', max_digits=12, decimal_places=2)),
                ('part_quantity', models.IntegerField(verbose_name=b'Quantity')),
                ('employee', models.ForeignKey(verbose_name=b'Technician', to='employee.employee')),
                ('equipment_ID', models.ForeignKey(verbose_name=b'Equipment ID', to='equipment.EquipmentInfo')),
                ('part_supplier', models.ForeignKey(verbose_name=b'Part Supplier', to='supplier.supplier')),
            ],
            options={
                'verbose_name': 'Repair Equipment',
                'verbose_name_plural': 'Repair Equipment',
            },
        ),
        migrations.CreateModel(
            name='EquipmentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('equipment_type', models.CharField(max_length=50, verbose_name=b'Equipment Type')),
            ],
            options={
                'verbose_name': 'Equipment Type',
                'verbose_name_plural': 'Equipment Types',
            },
        ),
        migrations.CreateModel(
            name='PM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pm_item', models.CharField(max_length=50)),
                ('equipment_type', models.ForeignKey(verbose_name=b'Equipment Type', to='equipment.EquipmentType')),
            ],
            options={
                'verbose_name': 'Preventative Maintenance Item',
                'verbose_name_plural': 'Preventative Maintenance Items',
            },
        ),
        migrations.CreateModel(
            name='PMFreq',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pm_frequency', models.CharField(max_length=25, verbose_name=b'PM Frequency')),
            ],
            options={
                'verbose_name': 'Preventative Maintenance Frequency',
                'verbose_name_plural': 'Preventative Maintenance Frequencies',
            },
        ),
        migrations.AddField(
            model_name='pm',
            name='pm_frequency',
            field=models.ForeignKey(verbose_name=b'PM Frequency', to='equipment.PMFreq'),
        ),
        migrations.AddField(
            model_name='equipmentpm',
            name='logged_pm',
            field=models.ManyToManyField(to='equipment.PM', verbose_name=b'PM Items'),
        ),
        migrations.AddField(
            model_name='equipmentpm',
            name='pm_frequency',
            field=models.ForeignKey(verbose_name=b'PM Frequency', to='equipment.PMFreq'),
        ),
        migrations.AddField(
            model_name='equipmentinfo',
            name='equipment_type',
            field=models.ForeignKey(verbose_name=b'Equipment Type', to='equipment.EquipmentType'),
        ),
        migrations.AddField(
            model_name='equipmentinfo',
            name='manufacturer_name',
            field=models.ForeignKey(verbose_name=b'Manufacturer Name', to='equipment.EquipmentManufacturer'),
        ),
    ]
