# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-13 18:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_operation', '0002_auto_20180202_2059'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfav',
            unique_together=set([('user', 'goods')]),
        ),
    ]
