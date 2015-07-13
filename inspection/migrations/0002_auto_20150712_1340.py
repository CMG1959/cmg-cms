# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employee_shift_id'),
        ('startupshot', '0001_initial'),
        ('equipment', '0001_initial'),
        ('part', '0002_auto_20150712_1340'),
        ('inspection', '0001_initial'),
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
                ('inspectorName', models.ForeignKey(related_name='ct_inspectorName', verbose_name=b'Inspector Name', to='employee.employee')),
                ('jobID', models.ForeignKey(related_name='ct_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator', models.ForeignKey(related_name='ct_machineOperator', verbose_name=b'Machine Operator', to='employee.employee')),
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
                ('inspectorName', models.ForeignKey(related_name='ndi_inspectorName', verbose_name=b'Inspector Name', to='employee.employee')),
                ('jobID', models.ForeignKey(related_name='ndi_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator', models.ForeignKey(related_name='ndi_machineOperator', verbose_name=b'Machine Operator', to='employee.employee')),
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
                ('inspectorName', models.ForeignKey(related_name='odi_inspectorName', verbose_name=b'Inspector Name', to='employee.employee')),
                ('jobID', models.ForeignKey(related_name='odi_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator', models.ForeignKey(related_name='odi_machineOperator', verbose_name=b'Machine Operator', to='employee.employee')),
            ],
            options={
                'verbose_name': 'Outside Diameter Inspection',
                'verbose_name_plural': 'Outside Diameter Inspections',
            },
        ),
        migrations.CreateModel(
            name='visionInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('inspectorName', models.ForeignKey(related_name='vis_inspectorName', verbose_name=b'Inspector Name', to='employee.employee')),
                ('jobID', models.ForeignKey(related_name='vis_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator', models.ForeignKey(related_name='vis_machineOperator', verbose_name=b'Machine Operator', to='employee.employee')),
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
            name='volumeInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('liquidWeight', models.DecimalField(verbose_name=b'Liquid Weight (g)', max_digits=12, decimal_places=3)),
                ('inspectorName', models.ForeignKey(related_name='vol_inspectorName', verbose_name=b'Inspector Name', to='employee.employee')),
                ('jobID', models.ForeignKey(related_name='vol_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator', models.ForeignKey(related_name='vol_machineOperator', verbose_name=b'Machine Operator', to='employee.employee')),
            ],
            options={
                'verbose_name': 'Volume Inspection',
                'verbose_name_plural': 'Volume Inspections',
            },
        ),
        migrations.AlterField(
            model_name='visualinspection',
            name='inspectionResult',
            field=models.BooleanField(verbose_name=b'Inspection Result (check if passed)'),
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
            field=models.ForeignKey(related_name='assem_inspectorName', verbose_name=b'Inspector Name', to='employee.employee'),
        ),
        migrations.AddField(
            model_name='assemblyinspection',
            name='jobID',
            field=models.ForeignKey(related_name='assem_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot'),
        ),
        migrations.AddField(
            model_name='assemblyinspection',
            name='machineOperator',
            field=models.ForeignKey(related_name='assem_machineOperator', verbose_name=b'Machine Operator', to='employee.employee'),
        ),
    ]
