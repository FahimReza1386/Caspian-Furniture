from django.db import models
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField    
from decimal import Decimal
# Create your models here.

class SofaCategoryModel(models.Model):
    name= models.CharField(max_length=200)
    slug= models.SlugField(allow_unicode=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class SofaStatusType(models.IntegerChoices):
    publish = 1 , ("نمایش")
    draft = 2 , ("عدم نمایش")

class SofaColorsModel(models.Model):
    name=models.CharField(max_length=100)
    color= ColorField(default="#000000")

    def __str__(self):
        return self.name


class SofaBrandModel(models.Model):
    name=models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name



class SofaMaterialModel(models.Model):
    name=models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


WarrantyNumber = [
    (3, "۳ ماه"),
    (6, "۶ ماه"),
    (9, "۹ ماه"),
    (12, "12 ماه"),
    (16, "16 ماه"),
    (18, "18 ماه"),
    (22, "22 ماه"),
    (24, "24 ماه"),
                  ]


class SofaModel(models.Model):
    user= models.ForeignKey("accounts.User", on_delete=models.PROTECT)
    name= models.CharField(max_length=100)
    brand= models.ForeignKey(SofaBrandModel, on_delete=models.PROTECT)
    description = RichTextField(max_length=400)
    category= models.ManyToManyField(SofaCategoryModel)
    color=models.ManyToManyField(SofaColorsModel)
    stock= models.IntegerField()
    image=models.ImageField(upload_to="products/", null=True, blank=True)
    dimentions=models.CharField(max_length=50)
    material= models.ManyToManyField(SofaMaterialModel)
    price=models.DecimalField(default=0, max_digits=10, decimal_places=0)
    status=models.IntegerField(choices=SofaStatusType.choices, default=SofaStatusType.publish.value)
    discount_percent= models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    avg_rate=models.FloatField(default=0.0)
    Warranty=models.IntegerField(choices=WarrantyNumber, default=WarrantyNumber[0][0], null=True)
    weight= models.IntegerField(default=0, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

 
 
    def __str__(self):
        return self.name

    def is_discounted(self):
        return self.discount_percent != 0

    def get_price_after_sale(self):
        amout_price = self.price * Decimal(self.discount_percent/100)
        price= self.price - amout_price
        return round(price)


class SofaImageModel(models.Model):
    product = models.ForeignKey(SofaModel, on_delete=models.CASCADE)
    file= models.ImageField(upload_to="product/extra-img/")

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name