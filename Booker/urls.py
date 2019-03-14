from django.conf.urls import url
from Booker.views import SheetsView, ActivitiesView, CategoriesView

urlpatterns = [
    url('api_sheets', SheetsView.as_view()),
    url('api_activities',  ActivitiesView.as_view()),
    url('api_categories', CategoriesView.as_view())
    ]