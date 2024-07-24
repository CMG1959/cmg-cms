# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_auto_20151209_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='EmpLMName',
            field=models.CharField(default=b' ', max_length=20, null=True, verbose_name=b'First Name'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='EmpFName',
            field=models.CharField(max_length=50, null=True, verbose_name=b'First Name'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='EmpLName',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Last Name'),
        ),
    ]
