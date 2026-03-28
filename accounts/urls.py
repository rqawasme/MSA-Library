# accounts/urls.py
from django.urls import path

from accounts.forms import LoginForm

from django.views.generic import TemplateView

from .views import SignUpView, VerifyEmailView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(authentication_form=LoginForm), name="login"),
    path("verify/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify_email"),
    path("verification-sent/", TemplateView.as_view(template_name="registration/verification_sent.html"), name="verification_sent"),
]