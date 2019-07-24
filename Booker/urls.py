from django.conf.urls import url
from Booker.views import ActivitiesApi, SheetsApi

urlpatterns = [
    url('api/activities', ActivitiesApi.as_view()),
    url('api/sheets', SheetsApi.as_view()),
]