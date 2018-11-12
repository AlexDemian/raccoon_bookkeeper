# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm


class AuthForm(AuthenticationForm):

    def __init__(self):
        super(AuthForm, self).__init__()
        self.fields['username'].widget.attrs = {'class': 'form-control', 'value': 'example@domain.com'}
        self.fields['password'].widget.attrs = {'class': 'form-control', 'value': 'password'}

