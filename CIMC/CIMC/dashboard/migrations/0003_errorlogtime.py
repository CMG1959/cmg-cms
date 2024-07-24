# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20150930_0948'),
    ]

    operations = [
        migrations.CreateModel(
            name='errorLogTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number_of_days', models.IntegerField(default=1, verbose_name=b'Number of days to show errors:', validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
    ]
