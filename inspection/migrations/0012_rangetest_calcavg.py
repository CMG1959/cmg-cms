# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0011_auto_20150901_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='rangetest',
            name='calcAvg',
            field=models.BooleanField(default=False, verbose_name=b'Report raw data (do not take average)?'),
        ),
    ]
