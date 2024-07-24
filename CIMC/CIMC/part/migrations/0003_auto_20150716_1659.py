# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0002_auto_20150716_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partinspection',
            name='max_neck_diam',
            field=models.DecimalField(default=999999999, verbose_name=b'Maximum Neck Diameter', max_digits=12, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='partinspection',
            name='max_od',
            field=models.DecimalField(default=999999999, verbose_name=b'Maximum Outside Diameter', max_digits=12, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='partinspection',
            name='max_part_weight',
            field=models.DecimalField(default=999999999, verbose_name=b'Maximum Part Weight', max_digits=12, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='partinspection',
            name='max_vol',
            field=models.DecimalField(default=999999999, verbose_name=b'Maximum Volume', max_digits=12, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='partinspection',
            name='min_carton_tempt',
            field=models.DecimalField(default=999999999, verbose_name=b'Maximum Carton Temp', max_digits=12, decimal_places=3),
        ),
    ]
