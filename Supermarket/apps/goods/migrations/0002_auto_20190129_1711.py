# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-29 17:11
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsspu',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='商品详情'),
        ),
    ]