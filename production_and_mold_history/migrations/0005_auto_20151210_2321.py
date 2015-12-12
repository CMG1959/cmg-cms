# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production_and_mold_history', '0004_auto_20151210_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionhistory',
            name='jobNumber',
            field=models.CharField(max_length=20, verbose_name=b'Job Number', blank=True),
        ),
    ]
