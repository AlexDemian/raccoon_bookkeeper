# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.db import models

import uuid
import re




class User(AbstractUser):
    access_token = models.CharField(max_length=100, default=uuid.uuid4)
    confirmed = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

    def set_confirmed(self):
        self.confirmed = True
        self.save()

    def custom_save(self):
        from UserConfs.models import UserCategories, default_categories
        user = User.objects.create_user(username=self.username, password=self.password)
        user.save()
        for cat in default_categories:
            cat.update({'user': user})
            UserCategories(**cat).save()
        return user

    @staticmethod
    def username_valid(username, ajax=False):
        message = ''
        is_valid = True

        _taken = User.objects.filter(username__iexact=username).exists()
        if _taken:
            message = 'Username already taken.'
            is_valid = False

        try:
            validate_email(username)

        except ValidationError:
            message = 'Please make sure you enter a valid e-mail address.'
            is_valid = False

        if ajax:
            return JsonResponse({'is_valid': is_valid, 'message': message})

        elif not ajax and not is_valid:
            raise ValidationError(message)

    @staticmethod
    def password_valid(password, ajax=False):
        is_valid = re.search('^[a-zA-Z0-9]{7,20}$', password) is not None
        message = 'Password must be 7-20 latin characters/digits' if not is_valid else ''
        if ajax:
            return JsonResponse({'is_valid': is_valid, 'message': message})

        elif not ajax and not is_valid:
            raise ValidationError(message)


