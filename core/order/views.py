from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckOutForm
from .models import OrderItemModel, OrderModel, CouponModel, UserAddressModel
from datetime import timezone
from cart.models import CartModel
from django.http import JsonResponse
from cart.cart import CartSession
from decimal import Decimal
# Create your views here.

class OrderCheckoutView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "order/checkout.html"
    success_url = reverse_lazy("order:successfully")
    form_class = CheckOutForm

    def get_form_kwargs(self):
        kwargs= super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs
        
    def form_valid(self, form):
        user = self.request.user
        cleaned_data = form.cleaned_data
        address = cleaned_data["address_id"]
        coupon = cleaned_data["coupon"]
        cart = CartModel.objects.get(user=user)
        order= self.create_order(address)
        self.create_order_items(order,cart)
        self.clear_cart(cart)
        total_price = order.calculate_total_price()
        self.apply_coupon(coupon, order, user, total_price)
        order.save()
        return redirect(reverse_lazy("order:completed"))
        
    def create_order(self, address):
        order = OrderModel.objects.create(
            user=self.request.user,
            address=address.address,
            state=address.state,
            city= address.city,
            zip_code = address.zip_code
        )
        return order

    def create_order_items(self, order, cart):
        for item in cart.cart_items.all():
            OrderItemModel.objects.create(
                order = order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

    def apply_coupon(self, coupon, order, user, total_price):
        if coupon:
            discount_amount = round((total_price * Decimal(coupon.discount_percent / 100)))
            total_price -= discount_amount

            order.coupon = coupon
            coupon.used_by.add(user)
            coupon.save()
        order.total_price = total_price

    def get_context_data(self, **kwargs):
        cart= CartModel.objects.get(user=self.request.user)
        context= super().get_context_data(**kwargs) 
        context["addressess"] = UserAddressModel.objects.filter(user=self.request.user)
        total_price = cart.calculate_total_price()
        context["total_price"]= total_price
        total_tax = round((total_price * 10)/100)
        context["total_tax"] = total_tax
        total_payment_price = (int(total_price)+int(total_tax))
        context["total_payment_price"] = total_payment_price
        return context
    

    def create_payment_url(self):
        pass

    
    def clear_cart(self, cart):
        cart.cart_items.all().delete()
        CartSession(self.request.session).clear()


class OrderCompletedView(LoginRequiredMixin, TemplateView):
    template_name = "order/completed.html"

class OrderFailedView(LoginRequiredMixin, TemplateView):
    template_name = "order/failed.html"


class ValidationCouponView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        code = self.request.POST.get("coupon")

        status_code= 200
        message= "تخفیف با موفقیت اعمال شد ."
        total_price = 0
        total_tax = 0
        total_payment_price = 0

        user= self.request.user
        
        try :
            coupon = CouponModel.objects.get(code=code)
        except CouponModel.DoesNotExist:
            return JsonResponse({"message":"کد تخفیف وارد شده نا معتبر است ."}, status=404)
        
        else:
            if coupon.used_by.count() >= coupon.max_limit_usage:
                status_code, message=403, "محدودیت در تعداد استفاده کارکنان ."

            elif coupon.expiration_date and coupon.expiration_date < timezone.now():
                status_code, message=403, "مدت زمان استفاده از کد تخفیف به پایان رسیده است ."
            
            elif user in coupon.used_by.all():
                status_code, message = 403, "قبلا از کد تخفیف استفاده کرده اید ."

            else:
                cart = CartModel.objects.get(user=user)

                total_price = cart.calculate_total_price()
                total_price = round(total_price - (total_price * (Decimal(coupon.discount_percent)/100)))
                total_tax = round((total_price * 10) / 100)
                total_payment_price = round(total_price + total_tax)


        return JsonResponse({"message":message, "total_tax":total_tax, "total_price":total_price, "total_payment_price":total_payment_price}, status=status_code)