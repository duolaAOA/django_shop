# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-15 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0003_auto_20180413_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='city',
            field=models.CharField(default='', max_length=100, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='useraddress',
            name='province',
            field=models.CharField(default='', max_length=100, verbose_name='省份'),
        ),
        migrations.AlterUniqueTogether(
            name='userfav',
            unique_together=set([]),
        ),
    ]
