# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0001_initial'),
        ('molds', '0001_initial'),
        ('employee', '0001_initial'),
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MattecProd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jobNumber', models.CharField(max_length=15, verbose_name=b'Job Number')),
                ('machNo', models.CharField(max_length=10, verbose_name=b'Machine Number')),
                ('itemDesc', models.CharField(max_length=50, verbose_name=b'Item Description')),
                ('itemNo', models.CharField(max_length=15, verbose_name=b'Item Number')),
                ('moldNumber', models.CharField(max_length=15, verbose_name=b'Mold Number')),
                ('activeCavities', models.IntegerField(verbose_name=b'Active Cavities')),
                ('cycleTime', models.DecimalField(verbose_name=b'Cycle Time (s)', max_digits=12, decimal_places=3)),
            ],
            options={
                'verbose_name': 'MATTEC Current Job Information',
                'verbose_name_plural': 'MATTEC Current Job Information',
            },
        ),
        migrations.CreateModel(
            name='startUpShot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jobNumber', models.CharField(unique=True, max_length=15, verbose_name=b'Job Number')),
                ('activeCavities', models.IntegerField(verbose_name=b'Active Cavities')),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('shotWeight', models.DecimalField(verbose_name=b'Shot Weight', max_digits=12, decimal_places=3)),
                ('cycleTime', models.DecimalField(verbose_name=b'Cycle Time (s)', max_digits=12, decimal_places=3)),
                ('inspectorName', models.ForeignKey(verbose_name=b'Inspector Name', to='employee.Employees')),
                ('item', models.ForeignKey(verbose_name=b'Item', to='part.Part')),
                ('machNo', models.ForeignKey(verbose_name=b'Machine Number', to='equipment.EquipmentInfo')),
                ('moldNumber', models.ForeignKey(verbose_name=b'Mold Number', to='molds.Mold')),
            ],
            options={
                'verbose_name': 'Startup Shot',
                'verbose_name_plural': 'Startup Shots',
            },
        ),
    ]
