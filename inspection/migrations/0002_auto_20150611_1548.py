# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('startupshot', '0003_cimc_production_inproduction'),
        ('employee', '0001_initial'),
        ('inspection', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='partWeightInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'date published')),
                ('cavityID', models.CharField(max_length=5)),
                ('partWeight', models.DecimalField(max_digits=12, decimal_places=3)),
                ('inspectorName', models.ForeignKey(related_name='pwi_inspectorName', to='employee.employee')),
                ('jobID', models.ForeignKey(related_name='pwi_jobID', to='startupshot.CIMC_Production')),
                ('machineOperator', models.ForeignKey(related_name='pwi_machineOperator', to='employee.employee')),
            ],
        ),
        migrations.CreateModel(
            name='visualInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'date published')),
                ('inspectionResult', models.BooleanField()),
                ('cavityID', models.CharField(max_length=5)),
                ('partWeight', models.DecimalField(max_digits=12, decimal_places=3)),
            ],
        ),
        migrations.CreateModel(
            name='visualInspectionCriteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('defectType', models.CharField(max_length=25)),
            ],
        ),
        migrations.RemoveField(
            model_name='generalinspection',
            name='jobID',
        ),
        migrations.RemoveField(
            model_name='generalinspection',
            name='machineOperator',
        ),
        migrations.DeleteModel(
            name='generalInspection',
        ),
        migrations.AddField(
            model_name='visualinspection',
            name='defectType',
            field=models.ManyToManyField(to='inspection.visualInspectionCriteria'),
        ),
        migrations.AddField(
            model_name='visualinspection',
            name='inspectorName',
            field=models.ForeignKey(related_name='vi_inspectorName', to='employee.employee'),
        ),
        migrations.AddField(
            model_name='visualinspection',
            name='jobID',
            field=models.ForeignKey(related_name='vi_jobID', to='startupshot.CIMC_Production'),
        ),
        migrations.AddField(
            model_name='visualinspection',
            name='machineOperator',
            field=models.ForeignKey(related_name='vi_machineOperator', to='employee.employee'),
        ),
    ]
