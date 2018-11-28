# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import auth
from django.contrib.auth import authenticate

from .forms import AuthForm
from django import forms

from django.views import View

from django.db.models import signals
from django.contrib.auth.models import User
from booker.models import UserConfigs, UserCategories
from conf.tasks import send_verification_email


class Login(View):

    context = {
        'alerts': [],
        'auth_form': AuthForm(),
        'register_form': AuthForm()

    }

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/index")
        else:
            self.context['alerts'].append("Invalid login or password")

        return render(request, "login.html", self.context)

    def get(self, request):
        return render(request, "login.html", self.context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/auth/login")

class Register(View):
    default_categories = [
        ('meal', '-'),
        ('credit', '-'),
        ('utilities', '-'),
        ('salary', '+')
    ]


    def post(self, request):
        username, password = request.POST['username'], request.POST['password']

        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.save()

        user_confs = UserConfigs(user=user)
        user_confs.save()

        for cat in self.default_categories:
            category = UserCategories(user=user, name=cat[0], type=cat[1])
            category.save()

        user_id = User.objects.get(username=username).id
        send_verification_email.delay(user_id)
        return HttpResponseRedirect("/index")

class Verify(View):
    def post(self, request, uuid):
        try:
            user = User.objects.get(verification_uuid=uuid, is_verified=False)
        except User.DoesNotExist:
            pass
            #raise Http404("User does not exist or is already verified")

        user.is_verified = True
        user.save()

        return HttpResponseRedirect("/index")