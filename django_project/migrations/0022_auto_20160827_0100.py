# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-26 19:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_project', '0021_auto_20160823_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='deadline',
            field=models.DateField(default=datetime.date(2016, 9, 6), verbose_name='deadline'),
        ),
    ]
