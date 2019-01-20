# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-20 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=14)),
                ('password', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=20, null=True)),
                ('sex', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], default=2)),
                ('birthday', models.DateTimeField(null=True)),
                ('school', models.CharField(max_length=100, null=True)),
                ('location', models.CharField(max_length=100, null=True)),
                ('hometown', models.CharField(max_length=100, null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
