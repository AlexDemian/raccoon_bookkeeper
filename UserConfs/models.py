# -*- coding: utf-8 -*-
from Auth.models import User
from django.db import models

class UserCategories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=1)
    active = models.BooleanField(default=True)

    def get_user_categories(self, user_id):
        return [cat[0] for cat in self.objects.filter(user_id=user_id, active=True).values_list('name')]

    class Meta:
        db_table = 'user_confs'
