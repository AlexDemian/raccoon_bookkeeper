from django.conf.urls import url
from .views import SheetSettingsView, BsheetCreate, BsheetUpdate, BsheetDelete, CategoryCreate, CategoryUpdate, CategoryDelete, AccountSettingsView


urlpatterns = [
    url('add_category', CategoryCreate.as_view()),
    url('update_category', CategoryUpdate.as_view()),
    url('delete_category', CategoryDelete.as_view()),
    url('add_bsheet', BsheetCreate.as_view()),
    url('update_bsheet', BsheetUpdate.as_view()),
    url('delete_bsheet', BsheetDelete.as_view()),
    url('account_settings', AccountSettingsView.as_view()),
    url('sheet_settings', SheetSettingsView.as_view()),

]



