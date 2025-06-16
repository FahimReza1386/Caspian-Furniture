from rest_framework import serializers
from cart.models import CartItemModel, CartModel
from rest_framework.response import Response
from shop.models import SofaModel, SofaStatusType
from rest_framework import status

class SofaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SofaModel
        fields =["name", "price", "discount_percent"]

class CartItemsSerializer(serializers.ModelSerializer):
    product = SofaSerializer()

    class Meta:
        model = CartModel
        fields =["product", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    items= CartItemsSerializer(many=True)
    class Meta:
        model = CartModel
        fields =["items" , "user"]

    
class ListProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=0)
    product_id = serializers.IntegerField(source="product.id")
    product_sale_price = serializers.DecimalField(max_digits=10, decimal_places=0, source="product.get_price_after_sale")
    product_discount_percent = serializers.IntegerField(source="product.discount_percent")

    class Meta: 
        model = CartItemModel
        fields = ["product_name", "product_price", "product_id", "product_sale_price", "product_discount_percent", "quantity"]


class ProductCartSerializer(serializers.Serializer):
    product_id = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=True)


    def validate(self, attrs):
        product_id = attrs.get("product_id")
        quantity = attrs.get("quantity")
      
        try:
            product = SofaModel.objects.get(id=product_id)
            if product.status != SofaStatusType.publish.value:
                raise serializers.ValidationError({"product_id":"محصولی با این جزئیات وجود ندارد"})
            if quantity <= 0:
                raise serializers.ValidationError({"quantity":"تعداد سفارش باید بیشتر از 0 باشد ."})

            return attrs
    
        except SofaModel.DoesNotExist:
            raise serializers.ValidationError({"product_id":"محصولی با این شناسه وجود ندارد."})


class DeleteProductSerializer(serializers.Serializer):
    product_id = serializers.CharField(required=True)


    def validate(self, attrs):
        product_id = attrs.get("product_id")
      
        try:
            product = SofaModel.objects.get(id=product_id)
            if product.status != SofaStatusType.publish.value:
                raise serializers.ValidationError({"product_id":"محصولی با این جزئیات وجود ندارد"})
            return attrs
    
        except SofaModel.DoesNotExist:
            raise serializers.ValidationError({"product_id":"محصولی با این شناسه وجود ندارد."})
