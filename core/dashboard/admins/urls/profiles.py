from django.urls import path, include
from .. import views

urlpatterns=[
    path("security/edit/", views.AdminSecurityEdit.as_view(), name="security-edit"),
    path("profile/edit/", views.AdminProfileEdit.as_view(), name="profile-edit"),
    path("profile/image/edit/", views.AdminProfileImageEdit.as_view(), name="profile-image-edit"),
]
