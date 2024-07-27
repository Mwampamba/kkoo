from django.urls import path
from .import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_product_to_cart, name='add_to_cart'),
    path('remove-cart/<int:product_id>/<int:cart_product_id>/', views.remove_product_from_cart, name='remove_cart'),
    path('remove-cart-item/<int:product_id>/<int:cart_product_id>/', views.delete_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
]
