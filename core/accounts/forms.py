from django import forms
from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class AuthenticationsForm(auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        super(AuthenticationsForm, self).confirm_login_allowed(user)

        if not user.is_verified:
            raise ValidationError(_("your user not verified ."))
        

class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(max_length=200)
    class Meta:
        model = User
        fields = ("email", "password")
