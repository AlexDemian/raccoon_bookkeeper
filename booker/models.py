# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from auth_control.models import User

from unixtimestampfield.fields import UnixTimeStampField
from django.contrib.postgres.fields import ArrayField

import datetime
import time


class Activities(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    descr = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    price = models.FloatField(max_length=20)
    toggle = models.BooleanField(default=True)
    pinned = models.BooleanField(default=False)

    class Meta:
        db_table = 'costs'


class UserConfigs(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lang = models.CharField(max_length=5, default='eng')
    background = models.CharField(max_length=50, default='default_background.png')

    class Meta:
        db_table = 'user_confs'


class UserCategories(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=1, choices=(('+', 'earning'), ('-', 'cost')))
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_categories'
