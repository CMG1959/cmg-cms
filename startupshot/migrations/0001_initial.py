# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CIMC_Part',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_Number', models.CharField(max_length=15)),
                ('item_Description', models.CharField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='CIMC_Production',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jobNumber', models.CharField(max_length=15)),
                ('partWeight', models.DecimalField(max_digits=12, decimal_places=3)),
                ('cavityID', models.CharField(max_length=5)),
                ('headID', models.CharField(max_length=5)),
                ('activeCavities', models.IntegerField()),
                ('item', models.ForeignKey(to='startupshot.CIMC_Part')),
            ],
        ),
    ]
