# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    access_token = models.CharField(max_length=100)