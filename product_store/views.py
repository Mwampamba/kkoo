from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils.text import slugify
from product_catalog.models import Category, Brand
from product_order.models import ProductOrder
from .models import Product, ProductGallery, Rating
import os


def product_store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, category_slug=category_slug)
        products = Product.objects.filter(
            product_category=categories, status=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        total_products = products.count()

    else:
        products = Product.objects.all().filter(status=True).order_by('-selling_price')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        total_products = products.count()

    context = {
        'products': paged_products,
        'total_products': total_products
    }

    return render(request, 'product/store.html', context)


def product_detail(request, category_slug, product_slug):
    categories = None
    try:
        if category_slug != None:
            categories = get_object_or_404(Category, category_slug=category_slug)
            product = Product.objects.get(
                product_category__category_slug=category_slug, product_slug=product_slug)
        
        related_products = Product.objects.filter(
            product_category=categories, status=True).order_by('-created_at')[1:4]

    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = ProductOrder.objects.filter(
                user=request.user, product_id=product.id).exists()

        except ProductOrder.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    reviews = Rating.objects.filter(product_id=product.id, status=True).order_by('-created_at')[:5]
    reviews_count = reviews.count()

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=product.id)
    
    context = {
        'product': product,
        'related_products': related_products,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
        'reviews_count': reviews_count
    }

    return render(request, 'product/details.html', context)


def search_product(request):
    if 'q' in request.GET:
        keyword = request.GET['q']
        if keyword:
            products = Product.objects.order_by('id').filter(
                Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            total_products = products.count()

    context = {
        'products': paged_products,
        'total_products': total_products,
    }

    return render(request, 'product/store.html', context)


class RatingAndReview(View):
    def get(self, request):
        return render(request, 'product/details.html')

    def post(self, request, product_id):
        current_url = request.META.get('HTTP_REFERER')
        subject = request.POST.get('subject', False)
        review = request.POST.get('review', False)
        rate = request.POST.get('rating', False)
        product_id = product_id
        user_id = request.user.id

        Rating.objects.create(
            subject=subject, review=review, rate=rate, product_id=product_id, user_id=user_id, status=True)

        messages.success(request, 'Thank you! your review has been submited.')

        return redirect(current_url)

 
@login_required(login_url = 'login')
def products_by_vendor(request):
    products = Product.objects.filter(vendor=request.user).order_by('-created_at')
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
    }
    return render(request, 'product/crud/index.html', context)


@login_required(login_url = 'login')
def add_product(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()

    context = {
    'categories': categories,
    'brands': brands
    }
    
    if request.method == 'POST': 
        vendor = request.user
        product_name = request.POST['product_name'] 
        product_slug = slugify(product_name)
        category = request.POST['category']
        brand = request.POST['brand']
        description = request.POST['description']
        original_price = request.POST['original_price'] 
        selling_price = request.POST['selling_price']
        stock = request.POST['stock'] 
        status = request.POST['status']

        if len(request.FILES) != 0:
            picture = request.FILES['picture']

        product = Product(product_name=product_name,product_slug=product_slug,product_category_id=category,product_brand_id=brand,
                            product_description=description,product_image=picture,product_stock=stock,original_price=original_price,
                            selling_price=selling_price,vendor=vendor,status=status) 
            
        product.save()

        messages.success(request, 'Product has been saved')

        

        return redirect('products_by_vendor')

    return render(request, 'product/crud/create.html', context)


@login_required(login_url = 'login')
def update_product(request, pk):
    product = Product.objects.get(id=pk) 
    categories = Category.objects.all()
    brands = Brand.objects.all()

    context = {
        'product': product,
        'categories': categories,
        'brands': brands
    }
    
    if request.method == 'POST': 
        if len(request.FILES) != 0:
            if len(product.product_image) > 0:
                os.remove(product.product_image.path)
            vendor = request.user
            product_name = request.POST['product_name'] 
            product_slug = slugify(product_name) + 'q'
            category = request.POST['category']
            brand = request.POST['brand']
            description = request.POST['description']
            original_price = request.POST['original_price'] 
            selling_price = request.POST['selling_price']
            stock = request.POST['stock'] 
            status = request.POST['status']
            
            picture = request.FILES['picture']

        product = Product(product_name=product_name,product_slug=product_slug,product_category_id=category,product_brand_id=brand,
                            product_description=description,product_image=picture,product_stock=stock,original_price=original_price,
                            selling_price=selling_price,vendor=vendor,status=status) 
            
        product.save()

        messages.success(request, 'Product has been updated')

        return redirect('products_by_vendor')

    return render(request, 'product/crud/update.html', context)


@login_required(login_url = 'login')
def delete_product(request, pk):
    
    product = Product.objects.get(id=pk) 
    product.delete()

    messages.success(request, 'Product has been deleted')

    return redirect('products_by_vendor')
