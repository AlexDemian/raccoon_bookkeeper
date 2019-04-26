# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from Auth.models import User
from UserConfs.models import SheetBases, UserCategories

from unixtimestampfield.fields import UnixTimeStampField
from django.contrib.postgres.fields import ArrayField

import datetime
import time


class Sheets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sheetbase = models.ForeignKey(SheetBases, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.CharField(max_length=1000)

    class Meta:
        db_table = 'booker_sheets'


class Activities(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sheet = models.ForeignKey(Sheets, on_delete=models.CASCADE)
    descr = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(UserCategories, on_delete=models.CASCADE)
    value = models.FloatField()
    active = models.BooleanField(default=True)
    pinned = models.BooleanField(default=False)

    class Meta:
        db_table = 'booker_activities'




