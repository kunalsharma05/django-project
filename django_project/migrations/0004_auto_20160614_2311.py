# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-14 23:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django_project.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_project', '0003_auto_20160601_2057'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetsMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subname', models.CharField(max_length=255)),
                ('mimetype', models.CharField(blank=True, max_length=255, null=True)),
                ('asset_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DependeciesRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asset', to='django_project.AssetsMedia')),
                ('dependency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dependency', to='django_project.AssetsMedia')),
            ],
        ),
        migrations.CreateModel(
            name='MediaUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(upload_to=django_project.models.upload_manager)),
                ('mimetype', models.CharField(blank=True, max_length=255, null=True)),
                ('file_description', models.TextField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='django_project.Project')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='organisation',
            field=models.CharField(default='Peragro', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='milestone',
            name='deadline',
            field=models.DateField(default=datetime.date(2016, 6, 24), verbose_name='deadline'),
        ),
        migrations.AddField(
            model_name='dependeciesrelation',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_project.MediaUpload'),
        ),
        migrations.AddField(
            model_name='assetsmedia',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='django_project.MediaUpload'),
        ),
    ]
