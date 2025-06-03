from django.urls import path
from . import views


app_name = "api-rest"
urlpatterns = [
    # Login and Logout
    path("Token/login/", views.CustomObtainPaiAuthToken.as_view(), name="token/login"),
    path("Token/logout/", views.CustomObtainDiscardToken.as_view(), name="token/lohout"),
    path("jwt/login/", views.CustomObtainTokenPairView.as_view(), name="jwt/login"),
    path("jwt/refresh/", views.CustomTokenRefreshView.as_view(), name="jwt/refresh"),
    path("jwt/verify/", views.CustomTokenVerifyView.as_view(), name="jwt/verify"),
    path("register/", views.RegistrationApi.as_view(), name="register"),
    path("register/verify/<str:token>", views.RegisterVerify.as_view(), name="register/verify"),
]