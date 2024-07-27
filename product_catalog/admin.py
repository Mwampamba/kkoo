from django.contrib import admin
from .models import Category, Brand


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'category_slug': ('category_name',)}
    list_display = ('category_name',)
    list_per_page = 5


class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'brand_slug': ('brand_name',)}
    list_display = ('brand_name',)
    list_per_page = 5


admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
