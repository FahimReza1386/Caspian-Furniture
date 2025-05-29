from django.shortcuts import render
from django.contrib.auth import views as auth_views
from .forms import AuthenticationsForm

# Create your views here.


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationsForm
    redirect_authenticated_user = True

class LogoutView(auth_views.LogoutView):
    pass