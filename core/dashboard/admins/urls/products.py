from django.urls import path
from .. import views

urlpatterns = [
    path("product/list/", views.AdminProductsListView.as_view(), name="product-list"),
    path("product/edit/<int:pk>/", views.AdminProductsEditView.as_view(), name="product-edit"),
    path("product/delete/<int:pk>/", views.AdminProductDeleteView.as_view(), name="product-delete"),
    path("product/create/", views.AdminProductCreateView.as_view(), name="product-create"),
]