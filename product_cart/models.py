from django.db import models
from product_store.models import Product, Variation
from users.models import Account


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'cart'
        verbose_name = 'cart'
        verbose_name_plural = 'Cart'

    def __str__(self):
        return self.cart_id
    

class CartProduct(models.Model):
    product      = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation    = models.ManyToManyField(Variation, blank=True)
    user         = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    cart         = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity     = models.IntegerField()
    status       = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'cart_product'
        verbose_name = 'cartproduct'
        verbose_name_plural = 'Product in cart'
    
    def __unicode__(self):
        return self.product
    
    def sub_total(self):
        return self.product.selling_price * self.quantity
