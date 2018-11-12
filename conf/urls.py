"""person_inspector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.contrib.auth.decorators import login_required

from booker.views import Index
from conf.settings import STATIC_ROOT, STATIC_URL
from auth_control.urls import urlpatterns as auth_urlpatterns



urlpatterns = [
    url(r'^$|index', login_required(Index.as_view(), '')),
    url(r'^auth/', include(auth_urlpatterns)),
    ] + static(STATIC_URL, document_root=STATIC_ROOT)
