from django.urls import path
from . import views

app_name="website"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("contact/", views.ContactPageView.as_view(), name="contact"),
]   