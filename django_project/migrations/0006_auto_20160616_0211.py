# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-16 02:11
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_project', '0005_auto_20160615_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='deadline',
            field=models.DateField(default=datetime.date(2016, 6, 26), verbose_name='deadline'),
        ),
    ]
