# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('EmpNum', models.CharField(max_length=25, verbose_name=b'Employee Number')),
                ('EmpLName', models.CharField(max_length=25, verbose_name=b'Last Name')),
                ('EmpFName', models.CharField(max_length=25, verbose_name=b'First Name')),
                ('EmpManNum', models.CharField(max_length=25, verbose_name=b'Employee Man Number')),
                ('EmpShift', models.IntegerField(verbose_name=b'Shift')),
            ],
            options={
                'verbose_name': 'Employee Information',
                'verbose_name_plural': 'Employee Information',
            },
        ),
        migrations.CreateModel(
            name='JobTitles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('JobNum', models.IntegerField(verbose_name=b'Job Number')),
                ('JobTitle', models.CharField(max_length=25, verbose_name=b'Job Title')),
            ],
            options={
                'verbose_name': 'Job Titles',
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.AddField(
            model_name='employees',
            name='EmpJob',
            field=models.ForeignKey(verbose_name=b'Employee Job Title', to='employee.JobTitles'),
        ),
    ]
