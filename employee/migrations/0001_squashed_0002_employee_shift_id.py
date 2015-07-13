# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    replaces = [(b'employee', '0001_initial'), (b'employee', '0002_employee_shift_id')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_name', models.CharField(max_length=25, verbose_name=b'Last Name')),
                ('first_name', models.CharField(max_length=25, verbose_name=b'First Name')),
                ('employee_id', models.CharField(max_length=25, verbose_name=b'Employee ID')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
            },
        ),
        migrations.CreateModel(
            name='organizations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('org_name', models.CharField(max_length=25, verbose_name=b'Organization Name')),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='organization_name',
            field=models.ForeignKey(verbose_name=b'Organization Name', to='employee.organizations'),
        ),
        migrations.AddField(
            model_name='employee',
            name='shift_id',
            field=models.IntegerField(default=1, verbose_name=b'Shift'),
        ),
    ]
