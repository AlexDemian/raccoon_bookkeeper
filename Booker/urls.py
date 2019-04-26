from django.conf.urls import url
from Booker.views import SheetsView, SheetDelete, SheetCreate, ActivityDelete, ActivityAdd, ActivityUpdate

urlpatterns = [
    url('api_sheets', SheetsView.as_view()),
    url('delete_sheet', SheetDelete.as_view()),
    url('create_sheet', SheetCreate.as_view()),
    url('delete_activity', ActivityDelete.as_view()),
    url('add_activity', ActivityAdd.as_view()),
    url('update_activity', ActivityUpdate.as_view()),
    ]