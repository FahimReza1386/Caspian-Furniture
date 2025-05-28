from django import template
from shop.models import SofaModel, SofaStatusType
register = template.Library()

@register.inclusion_tag("includes/latest_products.html", takes_context=True)
def show_latest_product(context):
    request= context.get("request")
    latest_product = SofaModel.objects.filter(status=SofaStatusType.publish.value).distinct().order_by("-created_date")[:4]
    return {"latest_products" : latest_product, "request":request}

@register.inclusion_tag("includes/similar_products.html", takes_context=True)
def show_similar_product(context, product):
    request= context.get("request")
    categories = product.category.all()
    similar_product = SofaModel.objects.filter(status=SofaStatusType.publish.value, category__in=categories).distinct().order_by("-created_date")[:4]
    return {"similar_products" : similar_product, "request":request}        