from django.shortcuts import render
from django.views.generic import ListView
from shop.models import SofaModel
from shop.models import SofaCategoryModel
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