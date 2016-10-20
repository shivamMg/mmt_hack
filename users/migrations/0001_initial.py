# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 06:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('countries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.SlugField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=15)),
                ('middle_name', models.CharField(blank=True, max_length=15)),
                ('last_name', models.CharField(blank=True, max_length=15)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='countries.Country')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]