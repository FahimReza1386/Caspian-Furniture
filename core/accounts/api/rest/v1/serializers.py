from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField()

    class Meta:
        model = User
        fields = ("email", "password", "password1")

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError(_("رمز عبور و تکرار آن باید یکسان باشند..."))
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password":list(e.messages)})
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop("password1", None)
        return super().create(validated_data)

class RegisterVerifySerializer(serializers.Serializer):
    pass

class TokenObtainPairViewSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_date = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"detail": "user is not verified ."})
        validated_date["email"] = self.user.email
        validated_date["user_id"] = self.user.id
        return validated_date


class CustomObtainPaiAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"), write_only=True)
    password = serializers.CharField(label=_("Password"), style={"input_type":"password"}, trim_whitespace=False, write_only=True)
    token =serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user= authenticate(request=self.context.get("request"), username=username, password=password)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                raise serializers.ValidationError({"detail": "user is not verified ."})
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")
        
        attrs["user"] = user
        return attrs