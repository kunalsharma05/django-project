# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-15 22:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_project', '0004_auto_20160614_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='position',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='deadline',
            field=models.DateField(default=datetime.date(2016, 6, 25), verbose_name='deadline'),
        ),
    ]
