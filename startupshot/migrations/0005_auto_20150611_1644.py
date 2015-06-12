# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startupshot', '0004_cimc_production_machno'),
    ]

    operations = [
        migrations.AddField(
            model_name='cimc_part',
            name='visual_inspection',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cimc_part',
            name='weight_inspection',
            field=models.BooleanField(default=True),
        ),
    ]
