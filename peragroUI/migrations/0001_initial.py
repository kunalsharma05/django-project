# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-18 00:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_project.models
import peragroUI.models
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_project', '0019_auto_20160818_0025'),
        ('auth', '0007_alter_validators_add_error_messages'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedResource_Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('effort', models.BigIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MediaUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(upload_to=peragroUI.models.upload_manager)),
                ('mimetype', models.CharField(blank=True, max_length=255, null=True)),
                ('file_description', models.TextField()),
                ('hash', models.CharField(db_index=True, max_length=128)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files_project', to='django_project.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('description', models.TextField()),
                ('profile_pic', models.ImageField(default='profile_pictures/user.png', upload_to='profile_pictures/')),
                ('organisation', models.CharField(max_length=256)),
                ('position', models.CharField(blank=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_project.Project', verbose_name='project')),
            ],
        ),
        migrations.CreateModel(
            name='TaskUI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('short_name', models.CharField(blank=True, max_length=126, null=True)),
                ('level', models.IntegerField(null=True)),
                ('summary', models.CharField(max_length=64, verbose_name='summary')),
                ('description', models.TextField(verbose_name='description')),
                ('status', models.CharField(default='STATUS_ACTIVE', max_length=256)),
                ('start', models.DateField(blank=True, help_text='YYYY-MM-DD', null=True, verbose_name='start')),
                ('end', models.DateField(blank=True, help_text='YYYY-MM-DD', null=True, verbose_name='end')),
                ('start_is_milestone', models.BooleanField(default=False)),
                ('end_is_milestone', models.BooleanField(default=False)),
                ('can_write', models.BooleanField(default=True)),
                ('has_child', models.BooleanField(default=False)),
                ('depends', models.CharField(blank=True, max_length=256, null=True)),
                ('collapsed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('component', smart_selects.db_fields.ChainedForeignKey(chained_field='project', chained_model_field='project', on_delete=django.db.models.deletion.CASCADE, to='django_project.Component', verbose_name='component')),
                ('priority', smart_selects.db_fields.ChainedForeignKey(chained_field='project', chained_model_field='project', on_delete=django.db.models.deletion.CASCADE, to='django_project.Priority', verbose_name='priority')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_project.Project', verbose_name='project')),
                ('type', smart_selects.db_fields.ChainedForeignKey(chained_field='project', chained_model_field='project', on_delete=django.db.models.deletion.CASCADE, to='django_project.TaskType', verbose_name='task type')),
            ],
        ),
        migrations.AddField(
            model_name='assignedresource_relation',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peragroUI.Role'),
        ),
        migrations.AddField(
            model_name='assignedresource_relation',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peragroUI.TaskUI'),
        ),
        migrations.AddField(
            model_name='assignedresource_relation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
