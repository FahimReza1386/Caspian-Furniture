from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from .validators import validate_iranian_phone_number

# Create your models here.


class UserType(models.IntegerChoices):
    customer= 1, _("Customer")
    admin= 2, _("Admin")
    superuser= 3, _("Superuser")

class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_field):
        if not email:
            raise ValueError("The Email must be set.")
        email= self.normalize_email(email=email)
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_field):
    
        extra_field.setdefault('is_active', True)
        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_verified', True)
        extra_field.setdefault('is_superuser', True)
        extra_field.setdefault('type', UserType.superuser.value)

        if extra_field.get("is_staff") is not True:
            raise ValueError(_("is staff must have is true."))

        if extra_field.get("is_active") is not True:
            raise ValueError(_("is active must have is true."))

        if extra_field.get("is_superuser") is not True:
            raise ValueError(_("is superuser must have is true."))
        
        return self.create_user(email, password, **extra_field)
    


class User(AbstractBaseUser,PermissionsMixin):
    email= models.EmailField(max_length=200, unique=True)
    is_staff= models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    is_superuser= models.BooleanField(default=False)
    is_verified= models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    type = models.IntegerField(choices=UserType.choices, default=UserType.customer.value)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # تغییر نام رابطه معکوس
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_permission_set',  # تغییر نام رابطه معکوس
        blank=True,
    )
    first_name = models.CharField(max_length=150)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=UserManager()

    def __str__(self):
        return self.email
    


class Gender(models.IntegerChoices):
    male= 1, _("male")
    female= 2, _("female")
    other= 3, _("other")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12, validators=[validate_iranian_phone_number])
    gender= models.IntegerField(choices=Gender.choices , default=Gender.other.value)
    image= models.ImageField(upload_to='profile/', default="profile/default.jpg")

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
    
    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"
    

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, pk=instance.pk)