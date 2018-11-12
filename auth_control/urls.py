from django.conf.urls import url
from django.contrib.staticfiles.urls import static
from .views import Login, logout, Register
from conf.settings import STATIC_ROOT, STATIC_URL

urlpatterns = [
    url('login', Login.as_view()),
    url('logout', logout),
    url('register', Register.as_view()),
    ] + static(STATIC_URL, document_root=STATIC_ROOT)