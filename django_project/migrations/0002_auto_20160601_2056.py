# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-01 20:56
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
        ('django_project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('description', models.TextField()),
                ('profile_pic', models.ImageField(default=b'profile_pictures/user.jpg', upload_to=b'profile_pictures/')),
            ],
        ),
        migrations.AlterField(
            model_name='milestone',
            name='deadline',
            field=models.DateField(default=datetime.date(2016, 6, 11), verbose_name='deadline'),
        ),
    ]
