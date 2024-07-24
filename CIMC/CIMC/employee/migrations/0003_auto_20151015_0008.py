# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_auto_20150715_1029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employees',
            name='EmpJob',
        ),
        migrations.AddField(
            model_name='employees',
            name='IsAdmin',
            field=models.BooleanField(default=False, verbose_name=b'Is Admin'),
        ),
        migrations.AddField(
            model_name='employees',
            name='IsMaintStaff',
            field=models.BooleanField(default=False, verbose_name=b'Is Maint Staff'),
        ),
        migrations.AddField(
            model_name='employees',
            name='IsMgmtStaff',
            field=models.BooleanField(default=False, verbose_name=b'Is Mgmt Staff'),
        ),
        migrations.AddField(
            model_name='employees',
            name='IsOpStaff',
            field=models.BooleanField(default=False, verbose_name=b'Is Ops Staff'),
        ),
        migrations.AddField(
            model_name='employees',
            name='IsPTLStaff',
            field=models.BooleanField(default=False, verbose_name=b'Is PTL Staff'),
        ),
        migrations.AddField(
            model_name='employees',
            name='IsQCStaff',
            field=models.BooleanField(default=False, verbose_name=b'Is QC Staff'),
        ),
        migrations.AddField(
            model_name='employees',
            name='IsSupervStaff',
            field=models.BooleanField(default=False, verbose_name=b'Is Supervisor Staff'),
        ),
        migrations.AddField(
            model_name='employees',
            name='IsToolStaff',
            field=models.BooleanField(default=False, verbose_name=b'Is Tool Staff'),
        ),
        migrations.AddField(
            model_name='employees',
            name='StatusActive',
            field=models.BooleanField(default=True, verbose_name=b'Status Active'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='EmpManNum',
            field=models.IntegerField(null=True, verbose_name=b'Employee Man Number'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='EmpNum',
            field=models.IntegerField(null=True, verbose_name=b'Employee Number'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='EmpShift',
            field=models.CharField(max_length=1, null=True, verbose_name=b'Shift'),
        ),
        migrations.DeleteModel(
            name='JobTitles',
        ),
    ]
