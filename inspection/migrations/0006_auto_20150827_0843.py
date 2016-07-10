# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0004_auto_20150721_1556'),
        ('startupshot', '0002_auto_20150721_1556'),
        ('molds', '0003_auto_20150721_1556'),
        ('employee', '0002_auto_20150715_1029'),
        ('inspection', '0005_auto_20150826_2113'),
    ]

    operations = [
        migrations.CreateModel(
            name='numericInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('isFullShot', models.BooleanField(default=True, verbose_name=b'Is Full Shot? (check if true)')),
                ('numVal', models.DecimalField(verbose_name=b'Test Value', max_digits=12, decimal_places=3)),
                ('headCavID', models.ForeignKey(verbose_name=b'Head and Cavity ID', blank=True, to='molds.PartIdentifier', null=True)),
                ('inspectorName', models.ForeignKey(related_name='ri_inspectorName', verbose_name=b'Inspector Name', to='employee.Employees')),
                ('jobID', models.ForeignKey(related_name='ri_jobID', verbose_name=b'Job ID', to='startupshot.startUpShot')),
                ('machineOperator', models.ForeignKey(related_name='ri_machineOperator', verbose_name=b'Machine Operator', to='employee.Employees')),
            ],
            options={
                'verbose_name': 'Range Inspection',
                'verbose_name_plural': 'Range Inspections',
            },
        ),
        migrations.CreateModel(
            name='numericTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('testName', models.CharField(unique=True, max_length=25, verbose_name=b'Range Test Name')),
            ],
            options={
                'verbose_name': 'Range Test Name',
                'verbose_name_plural': 'Range Test Names',
            },
        ),
        migrations.CreateModel(
            name='numericTestByPart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rangeMin', models.DecimalField(default=0, verbose_name=b'Minimum Value', max_digits=12, decimal_places=3)),
                ('rangeMax', models.DecimalField(default=0, verbose_name=b'Maximum Value', max_digits=12, decimal_places=3)),
                ('item_Number', models.ForeignKey(verbose_name=b'Part Number', to='part.Part')),
                ('testName', models.ForeignKey(verbose_name=b'Range Test Name', to='inspection.models.numericTest')),
            ],
            options={
                'verbose_name': 'Range Test Parameters By Part',
                'verbose_name_plural': 'Range Test Parameters By Parts',
            },
        ),
        migrations.AlterField(
            model_name='passfailtest',
            name='testName',
            field=models.CharField(unique=True, max_length=25, verbose_name=b'Pass Fail Test Name'),
        ),
        migrations.AlterUniqueTogether(
            name='passfailbypart',
            unique_together=set([('testName', 'item_Number')]),
        ),
        migrations.AlterUniqueTogether(
            name='passfailtestcriteria',
            unique_together=set([('testName', 'passFail')]),
        ),
        migrations.AddField(
            model_name='rangeinspection',
            name='numericTestName',
            field=models.ForeignKey(verbose_name=b'Inspection Name', to='inspection.models.numericTestByPart'),
        ),
        migrations.AlterUniqueTogether(
            name='rangetestbypart',
            unique_together=set([('testName', 'item_Number')]),
        ),
    ]
