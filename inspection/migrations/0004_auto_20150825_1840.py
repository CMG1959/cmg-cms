# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0003_auto_20150825_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passfailinspection',
            name='headCavID',
            field=models.ForeignKey(verbose_name=b'Head and Cavity ID', blank=True, to='molds.PartIdentifier', null=True),
        ),
    ]
