from django.contrib import admin
from .models import CartModel, CartItemModel
# Register your models here.

@admin.register(CartModel)
class CartModelAdmin(admin.ModelAdmin):
    list_display=["user", "created_date"]
    ordering = ["created_date"]
    search_fields= ["userــemail"]


@admin.register(CartItemModel)
class CartItemModelAdmin(admin.ModelAdmin):
    list_display=["product__name", "product__price", "quantity", "created_date"]
    ordering = ["created_date"]
    search_fields= ["product__price"]  