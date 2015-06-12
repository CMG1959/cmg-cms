# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startupshot', '0003_cimc_production_inproduction'),
    ]

    operations = [
        migrations.AddField(
            model_name='cimc_production',
            name='machNo',
            field=models.CharField(default='IMM01', max_length=6),
            preserve_default=False,
        ),
    ]
