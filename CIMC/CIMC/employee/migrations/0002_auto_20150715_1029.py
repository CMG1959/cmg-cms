# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='EmpFName',
            field=models.CharField(max_length=25, null=True, verbose_name=b'First Name'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='EmpLName',
            field=models.CharField(max_length=25, null=True, verbose_name=b'Last Name'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='EmpManNum',
            field=models.CharField(max_length=25, null=True, verbose_name=b'Employee Man Number'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='EmpShift',
            field=models.IntegerField(null=True, verbose_name=b'Shift'),
        ),
    ]
