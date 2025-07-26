from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile
from shop.models import SofaModel

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


class EditProductForm(forms.ModelForm):
    class Meta:
        model= SofaModel
        fields = ("name", "description", "stock", "price", "discount_percent","material", "dimentions", "category", "brand", "color", "status")
        widgets = {
            'material': forms.SelectMultiple(attrs={'class': 'form-select text-center'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-select text-center'}),
            'brand': forms.Select(attrs={'class': 'form-select text-center'}),
            'color': forms.SelectMultiple(attrs={'class': 'form-select text-center'}),
            'description': forms.Textarea(attrs={'class': 'form-control text-center'}),
        }

class CreateProductForm(forms.ModelForm):
    class Meta:
        model= SofaModel
        fields = ("name", "description", "stock", "price", "discount_percent","material", "dimentions", "category", "brand", "color", "status", "image")
        widgets = {
            'material': forms.SelectMultiple(attrs={'class': 'form-select text-center'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-select text-center'}),
            'brand': forms.Select(attrs={'class': 'form-select text-center'}),
            'color': forms.SelectMultiple(attrs={'class': 'form-select text-center'}),
            'description': forms.Textarea(attrs={'class': 'form-control text-center'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }