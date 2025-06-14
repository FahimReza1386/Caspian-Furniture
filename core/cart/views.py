from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .cart import CartSession
from cart.models import CartModel, CartItemModel
from django.http import JsonResponse
# Create your views here.


class CartSummaryView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart_summary.html"

    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        cart = CartSession(session=self.request.session)
        context["cart_items"] = cart.get_cart_items()
        context["total_quantity"] = cart.get_total_quantity()
        total_payment_price = cart.get_total_payment_price()
        context["total_payment_price"] = total_payment_price
        total_tax = round((cart.get_total_price()*10)/100)
        context["total_tax"] = total_payment_price - (total_payment_price - total_tax)
        context["total_price"] = cart.get_total_price()
        return context
    
class AddProductView(CreateView):
    
    def post(self, request, *args, **kwargs):
        cart = CartSession(session=request.session)
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("qty")
        if product_id and quantity:
            cart.add_product(product_id, quantity)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)

        return JsonResponse({"cart":cart.get_cart_dict(), "total_quantity":cart.get_total_quantity()})
    
class DeleteProductView(DeleteView):
    
    def post(self, request, *args, **kwargs):
        cart = CartSession(session=request.session)
        product_id = request.POST.get("product_id")
        if product_id:
            cart.delete_product(product_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)

        return JsonResponse({"cart":cart.get_cart_dict(), "total_quantity":cart.get_total_quantity()})

class UpdateProductQtyView(UpdateView):
    
    def post(self, request, *args, **kwargs):
        cart = CartSession(session=request.session)
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("qty")
        if product_id and quantity:
            cart.update_product_qty(product_id, quantity)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)

        return JsonResponse({"cart":cart.get_cart_dict(), "total_quantity":cart.get_total_quantity()})
    

