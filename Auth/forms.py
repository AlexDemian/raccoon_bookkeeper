# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm


class AuthForm(AuthenticationForm):

    def __init__(self):
        super(AuthForm, self).__init__()
        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'example@domain.com', 'id': 'id_signin_email'}
        self.fields['password'].widget.attrs = {'class': 'form-control', 'placeholder': 'password', 'id': 'id_signin_password'}

class RegisterForm(AuthenticationForm):

    def __init__(self):
        super(RegisterForm, self).__init__()
        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'example@domain.com', 'id': 'id_register_email'}
        self.fields['password'].widget.attrs = {'class': 'form-control', 'placeholder': 'password', 'id': 'id_register_password'}



