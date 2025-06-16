from django.contrib import admin
from .models import CouponModel, OrderModel, OrderItemModel, UserAddressModel 
# Register your models here.


@admin.register(CouponModel)
class CouponModelAdmin(admin.ModelAdmin):
    list_display = ("code", "expiration_date", "used_by_count", "max_limit_usage", "discount_percent")
    search_fields = ["code"]
    ordering = ["-created_date"]

    def used_by_count(self, obj): 
        return obj.used_by.all().count()

@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ("user", "total_price", "coupon", "status", "zip_code")
    search_fields = ["user"]
    ordering = ["-created_date"]

@admin.register(OrderItemModel)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ("order", "product__name", "quantity", "price")
    search_fields = ["product__name"]
    ordering = ["-created_date"]

@admin.register(UserAddressModel)
class UserAddressModelAdmin(admin.ModelAdmin):
    list_display = ("address", "city", "state", "zip_code")
    search_fields = ["address"]
    list_filter = ("city",)
    ordering = ["-created_date"]