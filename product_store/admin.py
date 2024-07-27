from django.contrib import admin
from .models import Product, Variation, Rating, ProductGallery
import admin_thumbnails


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'vendor', 'selling_price', 'product_stock',
                    'product_category', 'product_brand', 'status')
    prepopulated_fields = {'product_slug': ('product_name',)}
    inlines = [ProductGalleryInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'status')
    list_editable = ('status',)
    list_filter = ('product',)
    
    list_per_page = 5

class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('product', 'user', 'subject', 'review', 'rate', 'status')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(ProductGallery)

