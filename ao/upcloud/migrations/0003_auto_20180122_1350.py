# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-22 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upcloud', '0002_auto_20180122_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='zone',
            name='io_request_backup',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='zone',
            name='io_request_hdd',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='zone',
            name='io_request_maxiops',
            field=models.IntegerField(default=0),
        ),
    ]
