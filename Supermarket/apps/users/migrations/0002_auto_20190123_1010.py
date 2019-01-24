# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-23 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='head',
            field=models.ImageField(default='head/memtx.png', upload_to='head/%Y%m', verbose_name='用户头像'),
        ),
        migrations.AlterField(
            model_name='users',
            name='mobile',
            field=models.CharField(max_length=11, verbose_name='手机号码'),
        ),
    ]