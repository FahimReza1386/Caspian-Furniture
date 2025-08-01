from django.urls import path, include
from . import views

app_name="accounts"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("verify_url/<str:token>/", views.Verify_url.as_view(), name="verify_url"),
    path("api/v1/", include("accounts.api.rest.v1.urls")),
]