from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import TokenObtainPairViewSerializer, CustomObtainPaiAuthTokenSerializer, RegistrationSerializer, RegisterVerifySerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics
from accounts.models import User
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.urls import reverse
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt 


class RegistrationApi(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {
                "email" : email,
                "msg":"لینک فعال سازی اکانت شما ارسال شد .. ایمیل خود را چک کنید."
                }
            user = User.objects.get(email = email)
            payload = {
                "user_id" : user.id,
                "exp" : datetime.utcnow() + timedelta(hours=24),
                "iat" : datetime.utcnow()
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
            verify_url = self.request.build_absolute_uri(reverse("accounts:api-rest:register/verify", args=[token]))

            if email:
                email = EmailMessage('SendEmail Verified...', f"برای تایید ایمیل روی لینک زیر کلیک کنید:\n{verify_url}", "fahimweb.ir@gmail.com",[email])
                email.send()
            return Response(data=data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterVerify(generics.GenericAPIView):
    serializer_class = RegisterVerifySerializer
    def get(self, request,token, *args, **kwargs):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user_id = payload.get("user_id")
            user= get_object_or_404(User , pk=user_id)
            if user:
                user.is_active = True
                user.is_verified = True
                user.save()
                return Response({"email":user.email, "msg":"user verify is successfully.."}, status=status.HTTP_200_OK)
            return Response({"msg":" کاربر یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except ExpiredSignatureError:
            return Response({"msg" : "لینک تایید منقضی شده است."})
        except (InvalidTokenError, Exception):
            return Response({"msg" : "لینک تایید نامعتبر است."})

      
class CustomObtainPaiAuthToken(ObtainAuthToken):
    serializer_class = CustomObtainPaiAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        user =serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token":token.key, "user_id":user.pk, "email":user.email }, status=status.HTTP_200_OK)

class CustomObtainDiscardToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class CustomObtainTokenPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairViewSerializer

class CustomTokenRefreshView(TokenRefreshView):
    pass
class CustomTokenVerifyView(TokenVerifyView):
    pass
