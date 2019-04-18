from django.conf.urls import url
from .views import SettingsView

urlpatterns = [
    url('', SettingsView.as_view())
]