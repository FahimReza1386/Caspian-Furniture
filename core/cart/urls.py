from django.urls import path
from . import views


app_name = "cart"
urlpatterns = [
    path("cart_summary/", views.CartSummaryView.as_view(), name="cart-summary"),
    path("add-product/", views.AddProductView.as_view(), name="add-product"),
    path("update-product-quantity/", views.UpdateProductQtyView.as_view(), name="update-product-qty"),
    path("delete-product/", views.DeleteProductView.as_view(), name="delete-product"),
]