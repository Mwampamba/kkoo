from django.contrib import admin
from .models import Payment, Order, ProductOrder

class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'is_ordered')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'order_total', 'order_date', 'status', 'is_ordered']
    list_filter = ['status', 'is_ordered']
    readonly_fields = ['user', 'order_number', 'payment', 'first_name', 'last_name', 'phone', 'email', 'city', 'address_line_1','address_line_2', 'country', 'order_note', 'order_total', 'tax', 'status', 'is_ordered', 'order_date']
    list_per_page = 10
    # inlines = [ProductOrderInline]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'payment_id', 'payment_method', 'status']
    readonly_fields = ['user','amount', 'payment_id', 'payment_method', 'status']


class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'product_price', 'quantity']
    readonly_fields = ['user', 'order', 'product', 'payment', 'quantity', 'variation', 'is_ordered', 'product_price']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductOrder, ProductOrderAdmin)
