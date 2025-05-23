from django.urls import path
from .views import *

urlpatterns = [
    path("register/", UserLoginAPIView.as_view(), name="user-register"),
    path("login/", UserLoginAPIView.as_view(), name="user-login")
]