# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('molds', '0002_auto_20150715_1117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mold',
            options={'ordering': ('mold_number',), 'verbose_name': 'TMM Mold Information', 'verbose_name_plural': 'TMM Mold Information'},
        ),
    ]
