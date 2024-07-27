from django.contrib import admin
from .models import Cart, CartProduct


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'created_at')
    readonly_fields = ('cart_id', 'created_at')
    list_per_page = 5


class CartProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')
    readonly_fields = ('product', 'quantity', 'cart', 'status', 'user', 'variation')
    list_per_page = 5


# admin.site.register(Cart, CartAdmin)
# admin.site.register(CartProduct, CartProductAdmin)

