# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-06 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Booker', '0003_activities_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='descr',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]