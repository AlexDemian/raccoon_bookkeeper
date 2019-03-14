from django.conf.urls import include, url
from Booker.views import Index


urlpatterns = [
    url(r'^$|index', Index.as_view()),
    url(r'^auth/', include('Auth.urls')),
    url(r'^booker/', include('Booker.urls')),
    ]
