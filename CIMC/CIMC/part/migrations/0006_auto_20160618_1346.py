# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-18 17:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0005_auto_20150828_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='item_Number',
            field=models.CharField(max_length=15, unique=True, verbose_name=b'Item Number'),
        ),
    ]