# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('startupshot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cimc_production',
            name='dateCreated',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 5, 14, 9, 23, 800000, tzinfo=utc), verbose_name=b'date published'),
            preserve_default=False,
        ),
    ]
