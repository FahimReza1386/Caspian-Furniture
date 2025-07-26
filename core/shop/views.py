from django.shortcuts import render
from django.views.generic import ListView, DetailView
from shop.models import SofaModel, SofaCategoryModel, SofaStatusType, SofaImageModel
from django.core.exceptions import FieldError
from django.contrib import messages
# Create your views here.


class ProductGridView(ListView):
    template_name="shop/product-grid.html"
    paginate_by=9
    model=SofaModel

    def get_queryset(self):
        return super().get_queryset()
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = SofaCategoryModel.objects.all()
        return context

    

    def get_queryset(self):
        queryset =SofaModel.objects.filter(status=SofaStatusType.publish.value)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(name__icontains=search_q)

        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)

        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)

        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                messages.error(self.request , ("خطا در وارد کردن فیلد"))

        return queryset


class ProductDetailView(DetailView):
    template_name="shop/product-detail.html"
    queryset = SofaModel.objects.filter(status=SofaStatusType.publish.value).all()

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["extra_img"]=SofaImageModel.objects.filter(product__id=self.kwargs["pk"])
        return context