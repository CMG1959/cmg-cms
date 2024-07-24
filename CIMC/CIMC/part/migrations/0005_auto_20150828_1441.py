# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0004_auto_20150721_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partinspection',
            name='item_Number',
        ),
        migrations.DeleteModel(
            name='PartInspection',
        ),
    ]
