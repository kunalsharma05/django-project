# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-21 02:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_project', '0020_auto_20160821_0223'),
        ('peragroUI', '0002_uicomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignedresource_relation',
            name='project',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='django_project.Project', verbose_name='project'),
            preserve_default=False,
        ),
    ]
