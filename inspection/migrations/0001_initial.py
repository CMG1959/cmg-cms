# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startupshot', '0002_cimc_production_datecreated'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='generalInspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jobID', models.ForeignKey(to='startupshot.CIMC_Production')),
                ('machineOperator', models.ForeignKey(to='employee.employee')),
            ],
        ),
    ]
