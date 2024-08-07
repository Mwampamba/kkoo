from django.urls import reverse
from django.db import models
from product_catalog.models import Category, Brand
from users.models import Account
from django.db.models import Avg, Count
from djmoney.models.fields import MoneyField


class Product(models.Model):
    vendor = models.CharField(max_length=200) 
    product_name = models.CharField(max_length=200, unique=True)
    product_slug = models.SlugField(max_length=200, unique=True)
    product_description = models.TextField(max_length=500, blank=True)
    product_image = models.ImageField(upload_to='photos/products')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_stock = models.IntegerField()
    original_price = MoneyField(
        max_digits=14, decimal_places=2, default_currency='TZS')
    selling_price = MoneyField(
        max_digits=14, decimal_places=2, default_currency='TZS')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_detail', args=[self.product_category.category_slug, self.product_slug])

    
    class Meta:
        db_table = 'product'
        verbose_name = 'product'
        verbose_name_plural = 'Product'

    def __str__(self):
        return self.product_name 
    

    def average_review(self):
        reviews = Rating.objects.filter(product=self, status=True).aggregate(average=Avg('rate'))
        avg = 0

        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return round(avg, 1)


    def count_rating(self):
        reviews = Rating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count



class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', status=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', status=True)


variation_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100, choices=variation_choice)
    variation_value = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    objects = VariationManager()
    
    class Meta:
        db_table = 'variation'
        verbose_name = 'variation'
        verbose_name_plural = 'Size and Colour'

    def __str__(self):
        return self.variation_value



class Rating(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    user        = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject     = models.CharField(max_length=100, blank=True)
    review      = models.TextField(max_length=500, blank=True)
    rate        = models.FloatField()
    status      = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_rate'
        verbose_name = 'rating'
        verbose_name_plural = 'Rate and Review'


    def __str__(self):
        return self.subject



class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image   = models.ImageField(upload_to='store/products/', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'product gallery'
        verbose_name_plural = 'product gallery'