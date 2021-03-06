# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import auth, messages


from .forms import AuthForm, RegisterForm

from django.views import View

from .models import User

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from conf.settings import BASE_URL
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view



class AuthView(View):

    context = {
        'auth_form': AuthForm(),
        'register_form': RegisterForm()

    }

    def get(self, request):
        return render(request, "auth/login.html", self.context)

def logout(request):
    auth.logout(request)
    return redirect("/auth/signin_form")


def send_confirmation_letter(user_id, username, password, token):
    subject = 'Welcome to Raccoon Booker!'

    context = {
        'user_email': username,
        'user_password': password[:2] + '*' * (len(password) - 4) + password[-2:],
        'confirmation_url': '%s/auth/account_verification?uid=%s&token=%s' % (BASE_URL, user_id, token)
    }
    message = render_to_string('auth/confirmation_letter.html', context)

    letter = EmailMessage(subject, message, 'admin@raccoon_booker', [username])
    letter.content_subtype = 'html'
    letter.send()



def confirm_account(request):
    user = User.objects.get(id=request.GET["uid"])
    if request.GET["token"] == user.access_token:
        user.set_confirmed()
        messages.info(request, 'Account confirmed successfully!')
        auth.login(request, user)
        return redirect("/index")

    else:
        messages.info(request, 'Verification failed!')
        return redirect("/auth/signin_form")

def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        if not username or not password:
            return redirect("/auth/signin_form")

        user = User(username=request.POST["username"], password=request.POST["password"]).custom_save()

        messages.info(request, 'Account registered successfully. Please, check your mailbox (%s) for confirmation instructions' % user.username)
        send_confirmation_letter(user.id, username, password, user.access_token)
        auth.login(request, user)
    return redirect("/index")




def login(request):
    not_confirmed_message = 'Your account is not confirmed. Please check your mailbox for confirmation letter.'

    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:

            if not user.is_active:
                messages.error(request, "Error: account disabled")
                return redirect("/auth/signin_form")

            else:
                if not user.confirmed:
                    messages.info(request, not_confirmed_message)
                auth.login(request, user)
                return redirect("/index")
        else:

            messages.warning(request, 'Incorrect username and/or password')
            return redirect("/auth/signin_form")

    else:
        return redirect("/auth/signin_form")

@login_required
@api_view(['POST'])
def change_password(request):
    try:
        password = request.data["pass"]
        User().password_valid(password, ajax=False)
        request.user.set_password(password)
        return Response(status=status.HTTP_204_NO_CONTENT)

    except:
        return Response({'validationErrors': {'password': [User.password_invalid_message]}}, status=status.HTTP_200_OK)


def validate_username(request):
    return User().username_valid(request.GET["username"], ajax=True)


def validate_password(request):
    return User().password_valid(request.GET["password"], ajax=True)
