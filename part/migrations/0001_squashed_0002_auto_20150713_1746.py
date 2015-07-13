# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    replaces = [(b'part', '0001_initial'), (b'part', '0002_auto_20150713_1746')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_Number', models.CharField(max_length=15, verbose_name=b'Item Number')),
                ('item_Description', models.CharField(max_length=75, verbose_name=b'Item Description')),
                ('exp_part_weight',
                 models.DecimalField(verbose_name=b'Expected Part Weight', max_digits=12, decimal_places=3)),
                ('exp_cycle_time',
                 models.DecimalField(verbose_name=b'Expected Cycle Time', max_digits=12, decimal_places=3)),
            ],
            options={
                'verbose_name': 'Part',
                'verbose_name_plural': 'Parts',
            },
        ),
        migrations.CreateModel(
            name='PartInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visual_inspection', models.BooleanField(default=True, verbose_name=b'Visual Inspection')),
                ('part_weight_inspection', models.BooleanField(default=False, verbose_name=b'Part Weight Inspection')),
                ('shot_weight_inspection', models.BooleanField(default=True, verbose_name=b'Shot Weight Inspection')),
                ('item_Number', models.ForeignKey(verbose_name=b'Item Number', to='part.Part')),
                ('assembly_test_inspection',
                 models.BooleanField(default=False, verbose_name=b'Assembly Test Inspection')),
                ('carton_temp_inspection', models.BooleanField(default=False, verbose_name=b'Carton Temperature')),
                ('neck_diameter_inspection',
                 models.BooleanField(default=False, verbose_name=b'Neck Diameter Inspection')),
                ('od_inspection', models.BooleanField(default=False, verbose_name=b'Outside Diameter Inspection')),
                ('vision_system_inspection', models.BooleanField(default=False, verbose_name=b'Vision System')),
                ('vol_inspection', models.BooleanField(default=False, verbose_name=b'Volume Inspection')),
            ],
            options={
                'verbose_name': 'Required Part Inspection',
                'verbose_name_plural': 'Required Part Inspections',
            },
        ),
        migrations.AlterModelOptions(
            name='part',
            options={'verbose_name': 'TMM Part', 'verbose_name_plural': 'TMM Parts'},
        ),
    ]
