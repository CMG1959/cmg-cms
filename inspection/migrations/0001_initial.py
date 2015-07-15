# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0001_initial'),
        ('molds', '0001_initial'),
        ('employee', '0001_initial'),
        ('startupshot', '0001_initial'),
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='assemblyInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
            ],
            options={
                'verbose_name': 'Assembly Inspection',
                'verbose_name_plural': 'Assembly Inspections',
            },
        ),
        migrations.CreateModel(
            name='assemblyTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Assembly Test Criteria by Model',
                'verbose_name_plural': 'Assembly Test Criteria by Model',
            },
        ),
        migrations.CreateModel(
            name='assemblyTestCriteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assemblyTest', models.CharField(max_length=25, verbose_name=b'Test type')),
            ],
            options={
                'verbose_name': 'Assembly Test Criteria',
                'verbose_name_plural': 'Assembly Test Criteria',
            },
        ),
        migrations.CreateModel(
            name='cartonTemperature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('cartonTemp', models.DecimalField(verbose_name=b'Carton Temp (F)', max_digits=12, decimal_places=3)),
                ('inspectorName', models.ForeignKey(related_name='ct_inspectorName', verbose_name=b'Inspector Name', to='employee.Employees')),
                ('jobID', models.ForeignKey(related_name='ct_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator', models.ForeignKey(related_name='ct_machineOperator', verbose_name=b'Machine Operator', to='employee.Employees')),
            ],
            options={
                'verbose_name': 'Carton Temperature',
                'verbose_name_plural': 'Carton Temperatures',
            },
        ),
        migrations.CreateModel(
            name='neckDiameterInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('testResult', models.BooleanField(default=True, verbose_name=b'Test Result')),
                ('inspectorName', models.ForeignKey(related_name='ndi_inspectorName', verbose_name=b'Inspector Name', to='employee.Employees')),
                ('jobID', models.ForeignKey(related_name='ndi_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator', models.ForeignKey(related_name='ndi_machineOperator', verbose_name=b'Machine Operator', to='employee.Employees')),
            ],
            options={
                'verbose_name': 'Neck Diameter Inspection',
                'verbose_name_plural': 'Neck Diameter Inspections',
            },
        ),
        migrations.CreateModel(
            name='outsideDiameterInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('outsideDiameter', models.DecimalField(verbose_name=b'Outside Diameter', max_digits=12, decimal_places=3)),
                ('inspectorName', models.ForeignKey(related_name='odi_inspectorName', verbose_name=b'Inspector Name', to='employee.Employees')),
                ('jobID', models.ForeignKey(related_name='odi_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator', models.ForeignKey(related_name='odi_machineOperator', verbose_name=b'Machine Operator', to='employee.Employees')),
            ],
            options={
                'verbose_name': 'Outside Diameter Inspection',
                'verbose_name_plural': 'Outside Diameter Inspections',
            },
        ),
        migrations.CreateModel(
            name='partWeightInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('partWeight', models.DecimalField(verbose_name=b'Part Weight', max_digits=12, decimal_places=3)),
                ('headCavID', models.ForeignKey(verbose_name=b'Head and Cavity ID', to='molds.PartIdentifier')),
                ('inspectorName', models.ForeignKey(related_name='pwi_inspectorName', verbose_name=b'Inspector Name', to='employee.Employees')),
                ('jobID', models.ForeignKey(related_name='pwi_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator', models.ForeignKey(related_name='pwi_machineOperator', verbose_name=b'Machine Operator', to='employee.Employees')),
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
                ('activeCavities', models.IntegerField(default=1, verbose_name=b'Active Cavities')),
                ('inspectorName', models.ForeignKey(related_name='swi_inspectorName', verbose_name=b'Inspector Name', to='employee.Employees')),
                ('jobID', models.ForeignKey(related_name='swi_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator', models.ForeignKey(related_name='swi_machineOperator', verbose_name=b'Machine Operator', to='employee.Employees')),
            ],
            options={
                'verbose_name': 'Shot Weight Inspection',
                'verbose_name_plural': 'Shot Weight Inspections',
            },
        ),
        migrations.CreateModel(
            name='visionInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('inspectorName', models.ForeignKey(related_name='vis_inspectorName', verbose_name=b'Inspector Name', to='employee.Employees')),
                ('jobID', models.ForeignKey(related_name='vis_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator', models.ForeignKey(related_name='vis_machineOperator', verbose_name=b'Machine Operator', to='employee.Employees')),
            ],
            options={
                'verbose_name': 'Vision System Test',
                'verbose_name_plural': 'Vision System Test',
            },
        ),
        migrations.CreateModel(
            name='visionTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('equipmentID', models.ForeignKey(to='equipment.EquipmentInfo')),
            ],
            options={
                'verbose_name': 'Vision Test Criteria by Model',
                'verbose_name_plural': 'Vision Test Criteria by Model',
            },
        ),
        migrations.CreateModel(
            name='visionTestCriteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visionTest', models.CharField(max_length=25, verbose_name=b'Test type')),
            ],
            options={
                'verbose_name': 'Vision Test Criteria',
                'verbose_name_plural': 'Vision Test Criteria',
            },
        ),
        migrations.CreateModel(
            name='visualInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('inspectionResult', models.BooleanField(verbose_name=b'Inspection Result (check if passed)')),
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
        migrations.CreateModel(
            name='volumeInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('liquidWeight', models.DecimalField(verbose_name=b'Liquid Weight (g)', max_digits=12, decimal_places=3)),
                ('inspectorName', models.ForeignKey(related_name='vol_inspectorName', verbose_name=b'Inspector Name', to='employee.Employees')),
                ('jobID', models.ForeignKey(related_name='vol_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator', models.ForeignKey(related_name='vol_machineOperator', verbose_name=b'Machine Operator', to='employee.Employees')),
            ],
            options={
                'verbose_name': 'Volume Inspection',
                'verbose_name_plural': 'Volume Inspections',
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
            field=models.ForeignKey(related_name='vi_inspectorName', verbose_name=b'Inspector Name', to='employee.Employees'),
        ),
        migrations.AddField(
            model_name='visualinspection',
            name='jobID',
            field=models.ForeignKey(related_name='vi_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot'),
        ),
        migrations.AddField(
            model_name='visualinspection',
            name='machineOperator',
            field=models.ForeignKey(related_name='vi_machineOperator', verbose_name=b'Machine Operator', to='employee.Employees'),
        ),
        migrations.AddField(
            model_name='visiontest',
            name='visionTestItem',
            field=models.ForeignKey(to='inspection.visionTestCriteria'),
        ),
        migrations.AddField(
            model_name='visioninspection',
            name='visionTestResults',
            field=models.ManyToManyField(to='inspection.visionTest', verbose_name=b'Vision System Test Results'),
        ),
        migrations.AddField(
            model_name='assemblytest',
            name='assemblyTestItem',
            field=models.ForeignKey(to='inspection.assemblyTestCriteria'),
        ),
        migrations.AddField(
            model_name='assemblytest',
            name='part',
            field=models.ForeignKey(to='part.Part'),
        ),
        migrations.AddField(
            model_name='assemblyinspection',
            name='assemblyTestResults',
            field=models.ManyToManyField(to='inspection.assemblyTest', verbose_name=b'Assembly Test Results'),
        ),
        migrations.AddField(
            model_name='assemblyinspection',
            name='inspectorName',
            field=models.ForeignKey(related_name='assem_inspectorName', verbose_name=b'Inspector Name', to='employee.Employees'),
        ),
        migrations.AddField(
            model_name='assemblyinspection',
            name='jobID',
            field=models.ForeignKey(related_name='assem_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot'),
        ),
        migrations.AddField(
            model_name='assemblyinspection',
            name='machineOperator',
            field=models.ForeignKey(related_name='assem_machineOperator', verbose_name=b'Machine Operator', to='employee.Employees'),
        ),
    ]
