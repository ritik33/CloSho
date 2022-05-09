from django.contrib import admin
from .models import Category, Order, OrderItem, Product, ShippingAddress, Wishlist


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Wishlist)
