# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-10 11:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_project', '0011_auto_20160710_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='json_value',
            field=models.TextField(),
        ),
    ]
