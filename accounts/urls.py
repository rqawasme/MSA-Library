# accounts/urls.py
from django.urls import path

from accounts.forms import LoginForm

from .views import SignUpView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(authentication_form=LoginForm), name="login"),
]