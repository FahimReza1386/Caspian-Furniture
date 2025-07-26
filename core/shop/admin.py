from django.contrib import admin
from shop.models import SofaCategoryModel, SofaBrandModel, SofaModel, SofaColorsModel, SofaMaterialModel, SofaImageModel 
# Register your models here.


@admin.register(SofaModel)
class SofaModelAdmin(admin.ModelAdmin):
    list_display=("id", "name")

@admin.register(SofaBrandModel)
class SofaBrandModelAdmin(admin.ModelAdmin):
    list_display=("id", "name")

@admin.register(SofaMaterialModel)
class SofaMaterialModelAdmin(admin.ModelAdmin):
    list_display=("id", "name") 

@admin.register(SofaCategoryModel)
class SofaCategoryModelAdmin(admin.ModelAdmin):
    list_display=("id", "name")

@admin.register(SofaColorsModel)
class SofaColorsModelAdmin(admin.ModelAdmin):
    list_display=("id", "name")

@admin.register(SofaImageModel)
class SofaImageModelAdmin(admin.ModelAdmin):
    list_display=("id", "product")