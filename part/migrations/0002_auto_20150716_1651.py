# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='partinspection',
            name='max_neck_diam',
            field=models.DecimalField(default=0, verbose_name=b'Maximum Neck Diameter', max_digits=12, decimal_places=3),
        ),
        migrations.AddField(
            model_name='partinspection',
            name='max_od',
            field=models.DecimalField(default=0, verbose_name=b'Maximum Outside Diameter', max_digits=12, decimal_places=3),
        ),
        migrations.AddField(
            model_name='partinspection',
            name='max_part_weight',
            field=models.DecimalField(default=0, verbose_name=b'Maximum Part Weight', max_digits=12, decimal_places=3),
        ),
        migrations.AddField(
            model_name='partinspection',
            name='max_vol',
            field=models.DecimalField(default=0, verbose_name=b'Maximum Volume', max_digits=12, decimal_places=3),
        ),
        migrations.AddField(
            model_name='partinspection',
            name='min_carton_temp',
            field=models.DecimalField(default=0, verbose_name=b'Minimum Carton Temp', max_digits=12, decimal_places=3),
        ),
        migrations.AddField(
            model_name='partinspection',
            name='min_carton_tempt',
            field=models.DecimalField(default=0, verbose_name=b'Maximum Carton Temp', max_digits=12, decimal_places=3),
        ),
        migrations.AddField(
            model_name='partinspection',
            name='min_neck_diam',
            field=models.DecimalField(default=0, verbose_name=b'Minimum Neck Diameter', max_digits=12, decimal_places=3),
        ),
        migrations.AddField(
            model_name='partinspection',
            name='min_od',
            field=models.DecimalField(default=0, verbose_name=b'Minimum Outside Diameter', max_digits=12, decimal_places=3),
        ),
        migrations.AddField(
            model_name='partinspection',
            name='min_part_weight',
            field=models.DecimalField(default=0, verbose_name=b'Minimum Part Weight', max_digits=12, decimal_places=3),
        ),
        migrations.AddField(
            model_name='partinspection',
            name='min_vol',
            field=models.DecimalField(default=0, verbose_name=b'Minimum Volume', max_digits=12, decimal_places=3),
        ),
    ]
