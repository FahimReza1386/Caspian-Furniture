from django.urls import path
from . import views

app_name="api-rest"

urlpatterns = [
    path("list-product/", views.ListProductView.as_view(), name="list-product"),
    path("add-product/", views.AddProductView.as_view(), name="add-product"),
    path("update-product/", views.UpdateProductView.as_view(), name="update-product"),
    path("delete-product/", views.DeleteProductView.as_view(), name="delete-product"),
]