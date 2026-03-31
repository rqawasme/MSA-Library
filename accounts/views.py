# accounts/views.py
import os
import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic, View
from django.conf import settings
from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from accounts.models import User

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")

username_validator = UnicodeUsernameValidator()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=50, help_text='Required. Enter a valid email address.',  required=True,
                             widget=(forms.TextInput(attrs={'class': 'form-control'})))
    first_name = forms.CharField(max_length=20, min_length=2, required=True, help_text='Required: First Name',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=20, min_length=2, required=True, help_text='Required: Last Name',
                               widget=(forms.TextInput(attrs={'class': 'form-control'})))
    phone_number = forms.CharField(max_length=20, min_length=7, help_text='Required. Enter a valid phone number.', required=True,
                             widget=(forms.TextInput(attrs={'class': 'form-control'})))
    password1 = forms.CharField(label=_('Password'), required=False,
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label=_('Password Confirmation'), widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False,
                                help_text=_('Enter the same password, for confirmation'))
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2',)


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Build verification link
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(
            reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
        )

        requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
            json={
                "from": "MSA Library <verification@sfumsa.ca>",
                "to": [user.email],
                "subject": "Verify your MSA Library account",
                "text": f"Assalamu Alaikum {user.first_name},\n\nPlease verify your email by clicking this link:\n\n{verify_url}\n\nThis link expires in 3 days.\n\nJazakAllah Khair,\nSFU MSA Library",
            },
            timeout=10,
        )

        return redirect('verification_sent')


class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'registration/verification_success.html')
        else:
            return render(request, 'registration/verification_invalid.html')