from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductCartSerializer, DeleteProductSerializer, ListProductSerializer
from rest_framework import status
from cart.cart import CartSession
from cart.models import CartModel, CartItemModel


class ListProductView(ListAPIView): 
    serializer_class = ListProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            cart = CartModel.objects.get(user=user)
        except CartModel.DoesNotExist:
            return CartItemModel.objects.none()
        return CartItemModel.objects.filter(cart=cart)
        

class AddProductView(CreateAPIView):
    serializer_class = ProductCartSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        cart = CartSession(session=request.session)
        if serializer.is_valid(raise_exception=True):
            product_id = serializer.validated_data["product_id"]
            quantity = serializer.validated_data["quantity"]
            if product_id and quantity:
                cart.add_product(product_id, quantity)
                return Response({"detail":"محصول شما با موفقیت به سبد خرید اضافه شد ."}, status=status.HTTP_200_OK)
            if request.user.is_authenticated:
                cart.merge_session_cart_in_db(request.user)
            return Response({"detail":"خطایی رخ داد لطفا دقایقی بعد اقدام کنید .."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateProductView(UpdateAPIView):
    serializer_class = ProductCartSerializer
    permission_classes = [IsAuthenticated]

    def put(self,request):
        serializer = self.serializer_class(data=request.data)
        cart = CartSession(session=request.session)

        if serializer.is_valid(raise_exception=True):
            product_id = serializer.validated_data["product_id"]
            quantity = serializer.validated_data["quantity"]

            if product_id and quantity:
                cart.update_product_qty(product_id, quantity)
                return Response({"detail":"تعداد سفارش شما با موفقیت تغییر کرد."}, status=status.HTTP_200_OK)
            if request.user.is_authenticated:
                cart.merge_session_cart_in_db(request.user)
            return Response({"detail":"خطایی رخ داد دقایقی بعد مجددا تلاش کنید."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteProductView(DestroyAPIView):
    serializer_class = DeleteProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        cart = CartSession(session=request.session)
        
        if serializer.is_valid(raise_exception=True):
            product_id = serializer.validated_data["product_id"]

            if product_id:
                cart.delete_product(product_id)
                return Response({"detail":"محصول شما با موفقیت از سبد خرید حذف شد ."}, status=status.HTTP_200_OK)
            if request.user.is_authenticated:
                cart.merge_session_cart_in_db(request.user)
            return Response({"detail":"خطایی رخ داد لطفا دقایقی بعد اقدام کنید .."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.error_messages, status=status.HTTP_500_INTERNAL_SERVER_ERROR)