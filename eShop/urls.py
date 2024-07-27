from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .import views
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('admin/secure/', admin.site.urls),
    path('', views.home, name='home'),
    path('about-us', views.about_us, name='about_us'),
    path('terms-and-conditions', views.terms_and_conditions, name='terms_and_conditions'),
    path('', include(tf_urls)),
    path('authentication/', include('users.urls')),
    path('store/', include('product_store.urls')),
    path('cart/', include('product_cart.urls')),
    path('order/', include('product_order.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

