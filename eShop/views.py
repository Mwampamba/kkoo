from django.shortcuts import render
from product_store.models import Product


def home(request):
    products = Product.objects.all().filter(status=True).order_by('-selling_price')[:8]

    context = {
        'products': products
    }

    return render(request, 'home.html', context)


def terms_and_conditions(request):
    return render(request, 'terms.html')


def about_us(request):
    return render(request, 'about-us.html')
