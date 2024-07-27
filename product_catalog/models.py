from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    category_slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'Category'

    def get_url(self):
        return reverse('products_by_category', args=[self.category_slug])

    def __str__(self):
        return self.category_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=50, unique=True)
    brand_slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        db_table = 'brand'
        verbose_name = 'brand'
        verbose_name_plural = 'Brand'

    
    def get_url(self):
        return reverse('products_by_brand', args=[self.brand_slug])

    def __str__(self):
        return self.brand_name
