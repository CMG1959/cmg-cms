# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0003_auto_20150716_1659'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='part',
            options={'ordering': ('item_Number',), 'verbose_name': 'TMM Part', 'verbose_name_plural': 'TMM Parts'},
        ),
    ]
