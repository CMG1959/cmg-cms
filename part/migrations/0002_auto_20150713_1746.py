# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='part',
            options={'verbose_name': 'TMM Part', 'verbose_name_plural': 'TMM Parts'},
        ),
        migrations.AddField(
            model_name='partinspection',
            name='assembly_test_inspection',
            field=models.BooleanField(default=False, verbose_name=b'Assembly Test Inspection'),
        ),
        migrations.AddField(
            model_name='partinspection',
            name='carton_temp_inspection',
            field=models.BooleanField(default=False, verbose_name=b'Carton Temperature'),
        ),
        migrations.AddField(
            model_name='partinspection',
            name='neck_diameter_inspection',
            field=models.BooleanField(default=False, verbose_name=b'Neck Diameter Inspection'),
        ),
        migrations.AddField(
            model_name='partinspection',
            name='od_inspection',
            field=models.BooleanField(default=False, verbose_name=b'Outside Diameter Inspection'),
        ),
        migrations.AddField(
            model_name='partinspection',
            name='vision_system_inspection',
            field=models.BooleanField(default=False, verbose_name=b'Vision System'),
        ),
        migrations.AddField(
            model_name='partinspection',
            name='vol_inspection',
            field=models.BooleanField(default=False, verbose_name=b'Volume Inspection'),
        ),
    ]
