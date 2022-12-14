# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from accounts.models import User

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
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"