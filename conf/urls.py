from django.conf.urls import include, url
from rest_framework import routers
from django.urls import path
from Booker.views import Index
from django.shortcuts import render_to_response

def donate(request):
    return render_to_response('donate.html')


urlpatterns = [
    url('donate', donate),
    url(r'^$|index', Index.as_view()),
    url(r'^auth/', include('Auth.urls')),
    url(r'^booker/', include('Booker.urls')),
    url(r'^settings/', include('UserConfs.urls')),

    ]
