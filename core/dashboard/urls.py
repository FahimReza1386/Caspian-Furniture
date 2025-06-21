from django.urls import path, include
from . import views


app_name="dashboard"

urlpatterns =[
    path("home/", views.DashBoardHomeView.as_view(), name="home"),
    
    path("admin/", include("dashboard.admins.urls")),
    path("customer/", include("dashboard.customers.urls")),
]