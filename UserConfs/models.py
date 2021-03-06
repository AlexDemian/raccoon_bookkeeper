# -*- coding: utf-8 -*-
from django.db import models
from Auth.models import User

default_sheetbases = [
    {
        'name': 'Home',
        'categories':
            [
                {'name': 'meal', 'positive': False},
                {'name': 'fuel', 'positive': False},
                {'name': 'utilities', 'positive': False},
                {'name': 'salary', 'positive': True}
            ]
    }
]


categories_colors_palette = [
    '#ED9C33',
    '#191D32',
    '#282F44',
    '#453A49',
    '#3C7A89',
    '#CE796B',
    '#2E86AB',
    '#DAEFB3',
    '#B7FDFE',
    '#A80874',
    '#9E2A2B'
]


class SheetBases(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    autoadd = models.BooleanField(default=True)

    class Meta:
        db_table = 'booker_base_sheets'


class UserCategories(models.Model):
    sheetbase = models.ForeignKey(SheetBases, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    positive = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    color = models.CharField(null=True, max_length=100)

    def get_user_categories(self, user_id):
        return [cat[0] for cat in self.objects.filter(user_id=user_id, active=True).values_list('name')]

    class Meta:
        db_table = 'user_categories'
