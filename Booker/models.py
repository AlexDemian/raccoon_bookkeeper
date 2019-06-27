# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Count
from django.db.models.functions import Lower
from django.db.models import Avg

from Auth.models import User
from UserConfs.models import SheetBases, UserCategories

from unixtimestampfield.fields import UnixTimeStampField
from django.contrib.postgres.fields import ArrayField

import monthdelta
import datetime
import time

class Sheets(models.Model):
    name = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sheetbase = models.ForeignKey(SheetBases, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.CharField(max_length=1000)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'booker_sheets'

    def save(self, *args, **kwargs):
        self.name = self.sheetbase.name + ': ' + self.date.strftime('%B %Y')
        super(Sheets, self).save(*args, **kwargs)

        if self.sheetbase.autoadd:
            dt_now = datetime.datetime.now().date().replace(day=1)
            dt_from = dt_now - monthdelta.monthdelta(3)
            dt_to = dt_now + monthdelta.monthdelta(1)
            related_sheets = [s.pk for s in Sheets.objects.filter(sheetbase=self.sheetbase, date__range=(dt_from, dt_to))]
            qs = Activities.objects.filter(user=self.user, sheet__in=related_sheets).values('category')
            common_acts = qs.annotate(cnt=Count(Lower('name'))).values('name', 'category').filter(cnt__gte=3).annotate(avg_val=Avg('origin_value'))
            for act in common_acts:
                cat = UserCategories.objects.get(pk=act['category'])
                Activities(name=act['name'], value=int(act['avg_val']), category=cat, user=self.user, sheet=self).save()


class Activities(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sheet = models.ForeignKey(Sheets, on_delete=models.CASCADE)
    descr = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(UserCategories, on_delete=models.CASCADE)
    value = models.FloatField()
    origin_value = models.FloatField()
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'booker_activities'

    def save(self, *args, **kwargs):
        self.origin_value = self.value
        super(Activities, self).save(*args, **kwargs)


