# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-10 10:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_project', '0009_auto_20160710_0052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annotation',
            name='aspect_ratio',
        ),
    ]