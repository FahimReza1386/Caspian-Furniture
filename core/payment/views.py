from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import PaymentModel, PaymentStatusType
from order.models import OrderModel, OrderStatusType
from .zarinpal_client import ZarinPalBox
# Create your views here.


class PaymentVerifyView(View):

    def get(self, request, *args, **kwargs):
        authority_id = request.GET.get("Authority")
        payment_obj = get_object_or_404(PaymentModel, authority_id=authority_id)
        order = OrderModel.objects.get(payment=payment_obj)
        zarinpal = ZarinPalBox()
        response = zarinpal.payment_verify(int(payment_obj.amount), payment_obj.authority_id)
        data = response["data"]

        if data:
            if data["code"] == 100 or data["code"] == 101:
                payment_obj.ref_id = data["ref_id"]
                payment_obj.response_code = data["code"]
                payment_obj.status = PaymentStatusType.success.value
                payment_obj.response_json = response
                payment_obj.save()
                order.status = OrderStatusType.processing.value
                order.save()
                return redirect(reverse_lazy("order:completed"))
        else:
            payment_obj.status = PaymentStatusType.failed.value
            payment_obj.response_json = response
            payment_obj.save()
            order.status = OrderStatusType.canceled.value
            order.save()
            return redirect(reverse_lazy("order:failed"))
