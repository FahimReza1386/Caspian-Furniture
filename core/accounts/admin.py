from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from django.contrib.sessions.models import Session 
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model=User
    list_display =("email", "is_active", "is_superuser", "is_staff", "is_verified", "type")
    list_filter= ("is_staff", "is_superuser", "is_active", "is_verified", "type")
    searching_fields = ("email",)
    ordering =("email",)

    fieldsets = (
        ('Authentication', {
            "fields" : (
                "email", "password",
            )
        }),
        ('Permission', {
            "fields" : (
                "is_staff", "is_active", "is_superuser", "is_verified"
            )
        }),
        ('group permission', {
            "fields" : (
                'groups', 'user_permissions', 'type'
            )
        }),
        ('important date', {
            "fields": (
                "last_login",
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes' : ('wide',),
            'fields' : ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'type')
        }),
    )


class CustomProfileAdmin(admin.ModelAdmin):
    model= Profile
    list_display= ("id", "user", "first_name", "last_name", "phone_number", "gender")
    list_filter=("gender",)
    searching_fields= ('user', 'first_name', 'last_name', 'phone_number')


admin.site.register(Profile, CustomProfileAdmin)
admin.site.register(User, CustomUserAdmin)
