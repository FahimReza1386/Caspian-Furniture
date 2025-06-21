from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from accounts.models import UserType
from django.urls import reverse_lazy

# Create your views here.

class DashBoardHomeView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.type == UserType.customer.value:
                return redirect(reverse_lazy("dashboard:dash_customer:home"))
            if request.user.type == UserType.admin.value or UserType.superuser.value:
                return redirect(reverse_lazy("dashboard:dash_admin:home"))
        else:
            return redirect(reverse_lazy("accounts:login"))
        return super().dispatch(request, *args, **kwargs)