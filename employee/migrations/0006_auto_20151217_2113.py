# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_auto_20151215_1051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employees',
            old_name='DevTokenExpiry',
            new_name='DevTokenExpires',
        ),
    ]
