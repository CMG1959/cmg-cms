# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    replaces = [(b'molds', '0001_initial'), (b'molds', '0002_auto_20150710_1111')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mold',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mold_number', models.CharField(max_length=15, verbose_name=b'Mold Number')),
                ('mold_description', models.CharField(max_length=30, verbose_name=b'Mold Description')),
                ('num_cavities', models.IntegerField(verbose_name=b'Number of Cavities')),
            ],
            options={
                'verbose_name': 'Mold Information',
                'verbose_name_plural': 'Molds Information',
            },
        ),
        migrations.CreateModel(
            name='PartIdentifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('head_code', models.CharField(max_length=5, verbose_name=b'Head Code')),
                ('cavity_id', models.CharField(max_length=5, verbose_name=b'Cavity ID')),
                ('mold_number', models.ForeignKey(verbose_name=b'Mold Number', to='molds.Mold')),
            ],
        ),
        migrations.AlterModelOptions(
            name='mold',
            options={'verbose_name': 'TMM Mold Information', 'verbose_name_plural': 'TMM Mold Information'},
        ),
    ]
