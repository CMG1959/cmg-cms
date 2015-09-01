# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0009_auto_20150901_0742'),
    ]

    operations = [
        migrations.AddField(
            model_name='textinspection',
            name='inspectionResult',
            field=models.CharField(default=' ', max_length=75, verbose_name=b'Inspection Result (check if passed)'),
            preserve_default=False,
        ),
    ]
