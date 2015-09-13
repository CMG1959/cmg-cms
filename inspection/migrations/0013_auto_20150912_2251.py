# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0012_rangetest_calcavg'),
    ]

    operations = [
        migrations.AddField(
            model_name='rangeinspection',
            name='inspectionResult',
            field=models.BooleanField(default=False, verbose_name=b'Inspection Result (check if passed)'),
        ),
        migrations.AlterField(
            model_name='rangeinspection',
            name='numVal',
            field=models.DecimalField(verbose_name=b'Measurement', max_digits=12, decimal_places=3),
        ),
    ]
