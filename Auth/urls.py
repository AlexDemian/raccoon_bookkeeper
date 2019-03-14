from django.conf.urls import url
#from django.contrib.staticfiles.urls import static
from .views import login, logout, register, confirm_account, AuthView, validate_username, validate_password
#from conf.settings import STATIC_ROOT, STATIC_URL

urlpatterns = [
    url('signin_form', AuthView.as_view()),
    url('login', login),
    url('logout', logout),
    url('register', register),
    url('account_verification', confirm_account),
    url('validate_username', validate_username),
    url('validate_password', validate_password),
    ]