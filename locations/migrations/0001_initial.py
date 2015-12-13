# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='locations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('loc_ID', models.SmallIntegerField()),
                ('loc_Description', models.CharField(max_length=50)),
                ('loc_Country', models.CharField(max_length=2)),
                ('loc_Address_1', models.CharField(max_length=50)),
                ('loc_Address_2', models.CharField(max_length=50)),
                ('loc_City', models.CharField(max_length=50)),
                ('loc_ST', models.CharField(max_length=2)),
                ('loc_Zip', models.CharField(max_length=12)),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
    ]
