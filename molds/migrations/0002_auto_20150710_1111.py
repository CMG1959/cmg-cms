# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('molds', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mold',
            options={'verbose_name': 'TMM Mold Information', 'verbose_name_plural': 'TMM Mold Information'},
        ),
    ]
