from django.conf.urls import url
from Booker.views import SheetsView, SheetDelete, CategoriesView, ActivityDelete, ActivityAdd, ActivityUpdate

urlpatterns = [
    url('api_sheets', SheetsView.as_view()),
    url('delete_sheet', SheetDelete.as_view()),
    url('api_categories', CategoriesView.as_view()),
    url('delete_activity', ActivityDelete.as_view()),
    url('add_activity', ActivityAdd.as_view()),
    url('update_activity', ActivityUpdate.as_view()),
    ]