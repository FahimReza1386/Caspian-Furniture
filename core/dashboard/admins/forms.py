from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile

class AdminPasswordChangeForm(auth_forms.PasswordChangeForm):
    error_messages = {
        "password_mismatch": _("پسورد جدید و تکرار آن باید یکسان باشند ."),
        "password_incorrect": _(
            "پسورد فعلی شما اشتباه است اگر به یاد نمی اورید میتواند برای فراموش رمز عبور اقدام کنید."
        ),
    }

class AdminProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "phone_number", "gender"]


class AdminProfileImageEditForm(forms.Form):
    pass