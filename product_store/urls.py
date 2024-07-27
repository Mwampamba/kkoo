from django.urls import path
from .import views


urlpatterns = [
    path('', views.product_store, name='product_store'), 
    path('category/<slug:category_slug>/', views.product_store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search_product, name='search_product'),
    path('rate/<int:product_id>/', views.RatingAndReview.as_view(), name='rate_product'),
    path('products/', views.products_by_vendor, name='products_by_vendor'),
    path('add-product/', views.add_product, name='add_product'),
    path('update-product/<str:pk>', views.update_product, name='update_product'),
    path('delete-product/<str:pk>', views.delete_product, name='delete_product')
]
