from django.db import models
from users.models import Account
from product_store.models import Product, Variation
from djmoney.models.fields import MoneyField


class Payment(models.Model):
    user                = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount              = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    payment_id          = models.CharField(max_length=100) #transactionID
    payment_method      = models.CharField(max_length=100)
    status              = models.CharField(max_length=100)
    created_at          = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment'
        verbose_name = 'payment'
        verbose_name_plural = 'Payment'

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user            = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment         = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number    = models.CharField(max_length=20)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    phone           = models.CharField(max_length=15)
    email           = models.EmailField(max_length=50)
    address_line_1  = models.CharField(max_length=50)
    address_line_2  = models.CharField(max_length=50, blank=True)
    country         = models.CharField(max_length=50)
    city            = models.CharField(max_length=50)
    order_note      = models.CharField(max_length=100, blank=True)
    order_total     = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    tax             = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    status          = models.CharField(max_length=10, choices=STATUS, default='New')
    is_ordered      = models.BooleanField(default=False)
    order_date      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order'
        verbose_name = 'order'
        verbose_name_plural = 'Order'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.first_name



class ProductOrder(models.Model):
    user               = models.ForeignKey(Account, on_delete=models.CASCADE)
    order              = models.ForeignKey(Order, on_delete=models.CASCADE)
    product            = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment            = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    variation          = models.ManyToManyField(Variation, blank=True)
    quantity           = models.IntegerField()
    product_price      = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    is_ordered         = models.BooleanField(default=False)
    created_at         = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_order'
        verbose_name = 'payment'
        verbose_name_plural = 'Product Order'

    def __str__(self):
        return self.product.product_name