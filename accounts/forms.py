from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

class LoginForm(AuthenticationForm):
    password = forms.CharField(label=_('Password'), required=False, widget=(forms.PasswordInput))

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None:
            if password is None:
                password = ""
                
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data