# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('molds', '0003_auto_20150721_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='mold',
            name='loc_id',
            field=models.SmallIntegerField(default=10, verbose_name=b'Location ID'),
        ),
    ]
