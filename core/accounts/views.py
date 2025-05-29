import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import views as auth_views
from django.views.generic import View
from .forms import AuthenticationsForm
from accounts.models import User
from django.views.generic import CreateView
from .forms import RegisterForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail, EmailMessage
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
# Create your views here.


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationsForm
    redirect_authenticated_user = True

class LogoutView(auth_views.LogoutView):
    pass

class RegisterView(SuccessMessageMixin, CreateView):
    template_name = "accounts/register.html"
    model = User
    form_class = RegisterForm
    success_message = "لینک تایید ایمیل شما ارسال شد پس از کلیک روی لینک میتوانید وارد حساب کاربری خود شوید ."
    success_url = reverse_lazy("website:index")

    def form_valid(self, form):
        password = form.cleaned_data["password"]
        password2 = form.cleaned_data["password2"]
        if password != password2:
            form.add_error('password2', "رمز عبور و تکرار باید یکسان باشند ..")
            return self.form_invalid(form)
        user = form.save(commit=False)
        user.set_password(password2)
        user.save()
        
        payload = {
            "user_id" : user.id,
            "exp": datetime.utcnow() + timedelta(hours=24),
            "iat": datetime.utcnow()
        }

        token =jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        verify_url = self.request.build_absolute_uri(reverse("accounts:verify_url", args=[token]))

        email_address = form.cleaned_data.get("email")
        if email_address:
            email = EmailMessage('SendEmail Verified...', f"برای تایید ایمیل روی لینک زیر کلیک کنید:\n{verify_url}", "fahimweb.ir@gmail.com",[email_address])
            email.send()
        return super().form_valid(form)
    

class Verify_url(SuccessMessageMixin, View):
    def get(self, request, token, *args, **kwargs):
        try :
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            user = get_object_or_404(User, pk=user_id)
            user.is_verified = True
            user.save()
        except ExpiredSignatureError:
            messages.error(request, "لینک تایید منقضی شده است.")
        except (InvalidTokenError, Exception):
            messages.error(request, "لینک تایید نامعتبر است.")
        return redirect("website:index")    