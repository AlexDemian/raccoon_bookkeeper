# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-25 23:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Booker', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activities',
            old_name='price',
            new_name='value',
        ),
    ]