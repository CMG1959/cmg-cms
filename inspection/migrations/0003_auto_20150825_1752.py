# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0004_auto_20150721_1556'),
        ('startupshot', '0002_auto_20150721_1556'),
        ('molds', '0003_auto_20150721_1556'),
        ('employee', '0002_auto_20150715_1029'),
        ('inspection', '0002_auto_20150715_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='passFailByPart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_Number', models.ForeignKey(verbose_name=b'Part Number', to='part.Part')),
            ],
            options={
                'verbose_name': 'Pass Fail Test By Part',
                'verbose_name_plural': 'Pass Fail By Parts',
            },
        ),
        migrations.CreateModel(
            name='passFailInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('inspectionResult', models.BooleanField(default=True, verbose_name=b'Inspection Result (check if passed)')),
            ],
            options={
                'verbose_name': 'Pass Fail Inspection',
                'verbose_name_plural': 'Pass Fail Inspections',
            },
        ),
        migrations.CreateModel(
            name='passFailTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('testName', models.CharField(max_length=25, verbose_name=b'Pass Fail Test Name')),
            ],
            options={
                'verbose_name': 'Pass Fail Test Name',
                'verbose_name_plural': 'Pass Fail Test Names',
            },
        ),
        migrations.CreateModel(
            name='passFailTestCriteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('passFail', models.CharField(max_length=25, verbose_name=b'Pass Fail Reason')),
                ('testName', models.ForeignKey(verbose_name=b'Pass Fail Test Name', to='inspection.passFailTest')),
            ],
            options={
                'verbose_name': 'Pass Fail Test Criteria',
                'verbose_name_plural': 'Pass Fail Test Criteria',
            },
        ),
        migrations.AddField(
            model_name='passfailinspection',
            name='defectType',
            field=models.ManyToManyField(to='inspection.passFailTestCriteria', verbose_name=b'Defect Type', blank=True),
        ),
        migrations.AddField(
            model_name='passfailinspection',
            name='headCavID',
            field=models.ForeignKey(verbose_name=b'Head and Cavity ID', blank=True, to='molds.PartIdentifier'),
        ),
        migrations.AddField(
            model_name='passfailinspection',
            name='inspectorName',
            field=models.ForeignKey(related_name='pf_inspectorName', verbose_name=b'Inspector Name', to='employee.Employees'),
        ),
        migrations.AddField(
            model_name='passfailinspection',
            name='jobID',
            field=models.ForeignKey(related_name='pf_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot'),
        ),
        migrations.AddField(
            model_name='passfailinspection',
            name='machineOperator',
            field=models.ForeignKey(related_name='pf_machineOperator', verbose_name=b'Machine Operator', to='employee.Employees'),
        ),
        migrations.AddField(
            model_name='passfailinspection',
            name='passFailTestName',
            field=models.ForeignKey(verbose_name=b'Inspection Name', to='inspection.passFailTest'),
        ),
        migrations.AddField(
            model_name='passfailbypart',
            name='testName',
            field=models.ForeignKey(verbose_name=b'Pass Fail Test Name', to='inspection.passFailTest'),
        ),
    ]
