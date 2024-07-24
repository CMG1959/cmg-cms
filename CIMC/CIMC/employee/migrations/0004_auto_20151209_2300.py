# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_auto_20151015_0008'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='DevTokenExpiry',
            field=models.DateTimeField(null=True, verbose_name=b'Device Expire'),
        ),
        migrations.AddField(
            model_name='employees',
            name='DeviceToken',
            field=models.CharField(max_length=36, null=True, verbose_name=b'User GUID'),
        ),
    ]
