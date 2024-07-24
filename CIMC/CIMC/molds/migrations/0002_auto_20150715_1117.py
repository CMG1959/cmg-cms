# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('molds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mold',
            name='mold_description',
            field=models.CharField(max_length=50, verbose_name=b'Mold Description'),
        ),
        migrations.AlterField(
            model_name='mold',
            name='mold_number',
            field=models.CharField(max_length=20, verbose_name=b'Mold Number'),
        ),
    ]
