from django.urls import path, include

app_name = "dash_admin"

urlpatterns = [
    path("",include("dashboard.admins.urls.generals")),
    path("",include("dashboard.admins.urls.profiles")),
]