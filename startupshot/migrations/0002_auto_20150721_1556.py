# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_auto_20150715_1029'),
        ('startupshot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='startupshot',
            name='machineOperator',
            field=models.ForeignKey(related_name='sus_machineOperator', default=1, verbose_name=b'Machine Operator', to='employee.Employees'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='startupshot',
            name='inspectorName',
            field=models.ForeignKey(related_name='sus_inspectorName', verbose_name=b'Inspector Name', to='employee.Employees'),
        ),
    ]
