# -*- coding: utf-8 -*-
from django.db import models
from Auth.models import User

default_categories = [
    {'name': 'meal', 'positive': False},
    {'name': 'fuel', 'positive': False},
    {'name': 'utilities', 'positive': False},
    {'name': 'salary', 'positive': True},
]

class UserCategories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    positive = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def get_user_categories(self, user_id):
        return [cat[0] for cat in self.objects.filter(user_id=user_id, active=True).values_list('name')]

    class Meta:
        db_table = 'user_categories'
