from django.contrib import admin
from .models import Product, Customer, Cart


# Register your models here.


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','category','product_image']

@admin.register(Customer)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','zipcode','town']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

