# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-10 00:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_project', '0008_auto_20160618_0017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_value', models.TextField()),
                ('aspect_ratio', models.DecimalField(decimal_places=3, max_digits=5)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_project.Comment')),
            ],
        ),
        migrations.RemoveField(
            model_name='assetsmedia',
            name='file',
        ),
        migrations.RemoveField(
            model_name='dependenciesrelation',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='dependenciesrelation',
            name='dependency',
        ),
        migrations.RemoveField(
            model_name='dependenciesrelation',
            name='file',
        ),
        migrations.AlterField(
            model_name='mediaupload',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files_project', to='django_project.Project'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='deadline',
            field=models.DateField(default=datetime.date(2016, 7, 20), verbose_name='deadline'),
        ),
        migrations.DeleteModel(
            name='AssetsMedia',
        ),
        migrations.DeleteModel(
            name='DependenciesRelation',
        ),
    ]
