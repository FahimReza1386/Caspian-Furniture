from ...permissions import HasAdminAccessPermission
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from shop.models import SofaModel, SofaCategoryModel
from ..forms import EditProductForm, CreateProductForm
from django.core.exceptions import FieldError
from django.contrib import messages

class AdminProductsListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "dashboard/admin/products/product-list.html"
    model = SofaModel
    paginate_by = 10
    
    def get_paginate_by(self, queryset):
        valid_page_sizes = {5, 10, 20, 30}

        page_size_param = self.request.GET.get('page_size')

        try:
            page_size = int(page_size_param)
            if page_size > 0 or page_size in valid_page_sizes:
                return page_size
            else:
                return self.paginate_by
        except:
            return self.paginate_by

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["categories"] = SofaCategoryModel.objects.all()
        return context
    def get_queryset(self):
        queryset = SofaModel.objects.all().order_by("-created_date")
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(name__icontains=search_q)

        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)

        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                messages.error(self.request , ("خطا در وارد کردن فیلد"))

        return queryset
    


class AdminProductsEditView(LoginRequiredMixin, SuccessMessageMixin, HasAdminAccessPermission, UpdateView):
    template_name = "dashboard/admin/products/product-edit.html"
    form_class = EditProductForm
    model= SofaModel
    success_url = reverse_lazy("dashboard:dash_admin:product-list")
    success_message= "ادمین گرامی محصول شما با موفقیت ویرایش شد ."


class AdminProductDeleteView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    http_method_names="post"
    model=SofaModel
    success_url= reverse_lazy("dashboard:dash_admin:product-list")

    def get_success_message(self, cleaned_data):
        pk=self.kwargs["pk"]
        success_message= f"ادمین گرامی محصول با شناسه {pk} با موفقیت حذف شد .."
        return success_message
    

class AdminProductCreateView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, CreateView):
    model=SofaModel
    template_name="dashboard/admin/products/product-create.html"
    form_class= CreateProductForm
    success_message="ادمین گرامی محصول شما با موفقیت ساخته شد .."
    success_url=reverse_lazy("dashboard:dash_admin:product-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)