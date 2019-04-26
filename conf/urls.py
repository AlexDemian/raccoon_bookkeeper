from django.conf.urls import include, url
from rest_framework import routers
from django.urls import path
from Booker.views import Index


urlpatterns = [
    url(r'^$|index', Index.as_view()),
    url(r'^auth/', include('Auth.urls')),
    url(r'^booker/', include('Booker.urls')),
    url(r'^settings/', include('UserConfs.urls')),

    ]
