# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-26 23:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peragroUI', '0004_auto_20160827_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediaupload',
            name='resource_link',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]