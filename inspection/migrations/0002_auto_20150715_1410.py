# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assemblyinspection',
            name='inspectionResult',
            field=models.BooleanField(default=True, verbose_name=b'Inspection Result (check if passed)'),
        ),
        migrations.AddField(
            model_name='visioninspection',
            name='inspectionResult',
            field=models.BooleanField(default=True, verbose_name=b'Inspection Result (check if passed)'),
        ),
        migrations.AlterField(
            model_name='assemblyinspection',
            name='assemblyTestResults',
            field=models.ManyToManyField(to='inspection.assemblyTest', verbose_name=b'Assembly Test Results', blank=True),
        ),
        migrations.AlterField(
            model_name='visioninspection',
            name='visionTestResults',
            field=models.ManyToManyField(to='inspection.visionTest', verbose_name=b'Vision System Test Results', blank=True),
        ),
        migrations.AlterField(
            model_name='visualinspection',
            name='defectType',
            field=models.ManyToManyField(to='inspection.visualInspectionCriteria', verbose_name=b'Defect Type', blank=True),
        ),
        migrations.AlterField(
            model_name='visualinspection',
            name='inspectionResult',
            field=models.BooleanField(default=True, verbose_name=b'Inspection Result (check if passed)'),
        ),
    ]
