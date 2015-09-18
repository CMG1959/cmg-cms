# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0013_auto_20150912_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='passfailbypart',
            name='inspections_per_shift',
            field=models.IntegerField(default=2, verbose_name=b'Inspections Per Shift'),
        ),
        migrations.AddField(
            model_name='rangetestbypart',
            name='inspections_per_shift',
            field=models.IntegerField(default=2, verbose_name=b'Inspections Per Shift'),
        ),
        migrations.AddField(
            model_name='textrecordbypart',
            name='inspections_per_shift',
            field=models.IntegerField(default=2, verbose_name=b'Inspections Per Shift'),
        ),
    ]
