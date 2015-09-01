# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0010_textinspection_inspectionresult'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='passfailbypart',
            options={'verbose_name': 'Part Assignment - Pass Fail Test', 'verbose_name_plural': 'Part Assignment - Pass Fail Tests'},
        ),
        migrations.AlterModelOptions(
            name='passfailinspection',
            options={'verbose_name': 'Record - Pass Fail Inspection', 'verbose_name_plural': 'Record - Pass Fail Inspections'},
        ),
        migrations.AlterModelOptions(
            name='passfailtest',
            options={'verbose_name': 'Name - Pass Fail Test', 'verbose_name_plural': 'Name - Pass Fail Test'},
        ),
        migrations.AlterModelOptions(
            name='passfailtestcriteria',
            options={'verbose_name': 'Criteria - Pass Fail Test', 'verbose_name_plural': 'Criteria - Pass Fail Test'},
        ),
        migrations.AlterModelOptions(
            name='rangeinspection',
            options={'verbose_name': 'Record - Range Inspection', 'verbose_name_plural': 'Record - Range Inspections'},
        ),
        migrations.AlterModelOptions(
            name='rangetest',
            options={'verbose_name': 'Name - Range Test', 'verbose_name_plural': 'Name - Range Test'},
        ),
        migrations.AlterModelOptions(
            name='rangetestbypart',
            options={'verbose_name': 'Part Assignment - Range Test Parameters', 'verbose_name_plural': 'Part Assignment - Range Test Parameters'},
        ),
        migrations.AlterModelOptions(
            name='textinspection',
            options={'verbose_name': 'Record - Inspection', 'verbose_name_plural': 'Record - Text Inspections'},
        ),
        migrations.AlterModelOptions(
            name='textrecord',
            options={'verbose_name': 'Name - Text type Inspection', 'verbose_name_plural': 'Name - Text type Inspection'},
        ),
        migrations.AlterModelOptions(
            name='textrecordbypart',
            options={'verbose_name': 'Part Assignment - Text Test', 'verbose_name_plural': 'Part Assignment - Text Test'},
        ),
        migrations.AlterField(
            model_name='textinspection',
            name='inspectionResult',
            field=models.CharField(max_length=75, verbose_name=b'Enter Inspection Information:'),
        ),
    ]
