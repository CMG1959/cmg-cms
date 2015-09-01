# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0007_auto_20150827_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passfailtest',
            name='testName',
            field=models.CharField(unique=True, max_length=50, verbose_name=b'Pass Fail Test Name'),
        ),
        migrations.AlterField(
            model_name='passfailtestcriteria',
            name='passFail',
            field=models.CharField(max_length=50, verbose_name=b'Pass Fail Reason'),
        ),
        migrations.AlterField(
            model_name='rangetest',
            name='testName',
            field=models.CharField(unique=True, max_length=50, verbose_name=b'Range Test Name'),
        ),
    ]
