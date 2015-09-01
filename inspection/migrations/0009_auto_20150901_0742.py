# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0005_auto_20150828_1441'),
        ('startupshot', '0002_auto_20150721_1556'),
        ('molds', '0003_auto_20150721_1556'),
        ('employee', '0002_auto_20150715_1029'),
        ('inspection', '0008_auto_20150828_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='textInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('isFullShot', models.BooleanField(default=True, verbose_name=b'Is Full Shot? (check if true)')),
                ('headCavID', models.ForeignKey(verbose_name=b'Head and Cavity ID', blank=True, to='molds.PartIdentifier', null=True)),
                ('inspectorName', models.ForeignKey(related_name='ti_inspectorName', verbose_name=b'Inspector Name', to='employee.Employees')),
                ('jobID', models.ForeignKey(related_name='ti_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator', models.ForeignKey(related_name='ti_machineOperator', verbose_name=b'Machine Operator', to='employee.Employees')),
            ],
            options={
                'verbose_name': 'Text Inspection',
                'verbose_name_plural': 'Text Inspections',
            },
        ),
        migrations.CreateModel(
            name='textRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('testName', models.CharField(unique=True, max_length=75, verbose_name=b'Text Box Inspection Name')),
                ('requireAll', models.BooleanField(default=False, verbose_name=b'Require all parts get inspection?')),
            ],
            options={
                'verbose_name': 'Text Box Inspection',
                'verbose_name_plural': 'Text Box Inspection',
            },
        ),
        migrations.CreateModel(
            name='textRecordByPart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_Number', models.ForeignKey(verbose_name=b'Part Number', to='part.Part')),
                ('testName', models.ForeignKey(verbose_name=b'Text Test Name', to='inspection.textRecord')),
            ],
            options={
                'verbose_name': 'Text Test Parameters By Part',
                'verbose_name_plural': 'Text Test Parameters By Parts',
            },
        ),
        migrations.AddField(
            model_name='passfailtest',
            name='requireAll',
            field=models.BooleanField(default=False, verbose_name=b'Require all parts get inspection?'),
        ),
        migrations.AddField(
            model_name='rangetest',
            name='requireAll',
            field=models.BooleanField(default=False, verbose_name=b'Require all parts get inspection?'),
        ),
        migrations.AlterField(
            model_name='passfailtest',
            name='testName',
            field=models.CharField(unique=True, max_length=75, verbose_name=b'Pass Fail Test Name'),
        ),
        migrations.AlterField(
            model_name='passfailtestcriteria',
            name='passFail',
            field=models.CharField(max_length=75, verbose_name=b'Pass Fail Reason'),
        ),
        migrations.AlterField(
            model_name='rangetest',
            name='testName',
            field=models.CharField(unique=True, max_length=75, verbose_name=b'Range Test Name'),
        ),
        migrations.AddField(
            model_name='textinspection',
            name='textTestName',
            field=models.ForeignKey(verbose_name=b'Inspection Name', to='inspection.textRecord'),
        ),
        migrations.AlterUniqueTogether(
            name='textrecordbypart',
            unique_together=set([('testName', 'item_Number')]),
        ),
    ]
