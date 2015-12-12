# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production_and_mold_history', '0002_auto_20151210_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionhistory',
            name='shift',
            field=models.IntegerField(null=True, verbose_name=b'Shift', blank=True),
        ),
        migrations.AddField(
            model_name='productionhistory',
            name='shortDate',
            field=models.DateField(null=True, verbose_name=b'Short Date', blank=True),
        ),
    ]
