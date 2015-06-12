# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startupshot', '0002_cimc_production_datecreated'),
    ]

    operations = [
        migrations.AddField(
            model_name='cimc_production',
            name='inProduction',
            field=models.BooleanField(default=True),
        ),
    ]
