# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0002_equipmentinfo_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentpm',
            name='comments',
            field=models.CharField(max_length=1000, null=True, verbose_name=b'Event Description', blank=True),
        ),
        migrations.AddField(
            model_name='equipmentrepair',
            name='comments',
            field=models.CharField(max_length=1000, null=True, verbose_name=b'Event Description', blank=True),
        ),
    ]
