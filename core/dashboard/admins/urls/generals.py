from django.urls import path, include
from .. import views

urlpatterns=[
    path("home/", views.AdminDashBoardHomeView.as_view(), name="home"),
]
