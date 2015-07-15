# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('molds', '0001_initial'),
        ('employee', '0001_initial'),
        ('startupshot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoldHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('descEvent', models.CharField(max_length=1000, verbose_name=b'Event Description')),
                ('pm', models.BooleanField(default=False, verbose_name=b'Preventative Maintenance')),
                ('repair', models.BooleanField(default=False, verbose_name=b'Repair')),
                ('hours_worked', models.DecimalField(verbose_name=b'Hours worked', max_digits=10, decimal_places=2)),
                ('inspectorName', models.ForeignKey(verbose_name=b'Name', to='employee.Employees')),
                ('moldNumber', models.ForeignKey(verbose_name=b'Mold Number', to='molds.Mold')),
            ],
            options={
                'verbose_name': 'Mold History Log Entry',
                'verbose_name_plural': 'Mold History Log Entries',
            },
        ),
        migrations.CreateModel(
            name='ProductionHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('descEvent', models.CharField(max_length=1000, verbose_name=b'Event Description')),
                ('inspectorName', models.ForeignKey(verbose_name=b'Inspector Name', to='employee.Employees')),
                ('jobNumber', models.ForeignKey(verbose_name=b'Job Number', to='startupshot.startUpShot')),
            ],
            options={
                'verbose_name': 'Production History Log Entry',
                'verbose_name_plural': 'Production History Log Entries',
            },
        ),
    ]
