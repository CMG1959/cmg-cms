# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='errorLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shiftID', models.IntegerField(verbose_name=b'Shift')),
                ('dateCreated', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('machNo', models.CharField(max_length=10, verbose_name=b'Machine Number')),
                ('partDesc', models.CharField(max_length=50, verbose_name=b'Part Description')),
                ('jobID', models.CharField(max_length=10, verbose_name=b'Job ID')),
                ('inspectionName', models.CharField(max_length=50, verbose_name=b'Inspection Name')),
                ('errorDescription', models.CharField(max_length=250, verbose_name=b'Error Description')),
            ],
        ),
    ]
