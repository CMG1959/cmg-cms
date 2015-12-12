# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production_and_mold_history', '0003_auto_20151210_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionhistory',
            name='jobNumber',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Job Number', blank=True),
        ),
    ]
