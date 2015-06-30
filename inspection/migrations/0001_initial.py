# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('molds', '__first__'),
        ('startupshot', '__first__'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='partWeightInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('partWeight', models.DecimalField(verbose_name=b'Part Weight', max_digits=12, decimal_places=3)),
                ('headCavID', models.ForeignKey(verbose_name=b'Head and Cavity ID', to='molds.PartIdentifier')),
                ('inspectorName', models.ForeignKey(related_name='pwi_inspectorName', verbose_name=b'Inspector Name',
                                                    to='employee.employee')),
                ('jobID',
                 models.ForeignKey(related_name='pwi_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator',
                 models.ForeignKey(related_name='pwi_machineOperator', verbose_name=b'Machine Operator',
                                   to='employee.employee')),
            ],
            options={
                'verbose_name': 'Part Weight Inspection',
                'verbose_name_plural': 'Part Weight Inspections',
            },
        ),
        migrations.CreateModel(
            name='shotWeightInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('shotWeight', models.DecimalField(verbose_name=b'Shot Weight', max_digits=12, decimal_places=3)),
                ('inspectorName', models.ForeignKey(related_name='swi_inspectorName', verbose_name=b'Inspector Name',
                                                    to='employee.employee')),
                ('jobID',
                 models.ForeignKey(related_name='swi_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator',
                 models.ForeignKey(related_name='swi_machineOperator', verbose_name=b'Machine Operator',
                                   to='employee.employee')),
            ],
            options={
                'verbose_name': 'Shot Weight Inspection',
                'verbose_name_plural': 'Shot Weight Inspections',
            },
        ),
        migrations.CreateModel(
            name='visualInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('inspectionResult', models.BooleanField(verbose_name=b'Inspection Result')),
            ],
            options={
                'verbose_name': 'Visual Inspection',
                'verbose_name_plural': 'Visual Inspections',
            },
        ),
        migrations.CreateModel(
            name='visualInspectionCriteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('defectType', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name': 'Visual Inspection Criterion',
                'verbose_name_plural': 'Visual Inspection Criteria',
            },
        ),
        migrations.AddField(
            model_name='visualinspection',
            name='defectType',
            field=models.ManyToManyField(to='inspection.visualInspectionCriteria', verbose_name=b'Defect Type'),
        ),
        migrations.AddField(
            model_name='visualinspection',
            name='headCavID',
            field=models.ForeignKey(verbose_name=b'Head and Cavity ID', to='molds.PartIdentifier'),
        ),
        migrations.AddField(
            model_name='visualinspection',
            name='inspectorName',
            field=models.ForeignKey(related_name='vi_inspectorName', verbose_name=b'Inspector Name',
                                    to='employee.employee'),
        ),
        migrations.AddField(
            model_name='visualinspection',
            name='jobID',
            field=models.ForeignKey(related_name='vi_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot'),
        ),
        migrations.AddField(
            model_name='visualinspection',
            name='machineOperator',
            field=models.ForeignKey(related_name='vi_machineOperator', verbose_name=b'Machine Operator',
                                    to='employee.employee'),
        ),
    ]
