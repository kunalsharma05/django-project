# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-26 19:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peragroUI', '0003_assignedresource_relation_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskui',
            name='component',
        ),
        migrations.AlterField(
            model_name='assignedresource_relation',
            name='effort',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
