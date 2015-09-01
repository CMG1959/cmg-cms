# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0006_auto_20150827_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rangetestbypart',
            name='rangeMax',
            field=models.DecimalField(default=9999999, verbose_name=b'Maximum Value', max_digits=12, decimal_places=3),
        ),
    ]
