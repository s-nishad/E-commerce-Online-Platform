from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from product.core import AbstractBaseModel


class Category(AbstractBaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(AbstractBaseModel):
    categories = models.ForeignKey('product.Category', related_name='products', blank=True, null=True,
                                   on_delete=models.SET_NULL
                                   )
    product_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0)
    total_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product_name


class Stock(AbstractBaseModel):
    STOCK_TYPE_CHOICES = [
        ('IN', 'In'),
        ('OUT', 'Out')
    ]

    product = models.ForeignKey('product.Product', related_name='stocks', on_delete=models.CASCADE, null=True,
                                blank=True)
    quantity = models.PositiveIntegerField(default=0)
    stock_type = models.CharField(max_length=3, choices=STOCK_TYPE_CHOICES, default='IN')

    def __str__(self):
        return f"{self.product.product_name} - {self.get_stock_type_display()} {self.quantity}" if self.product else "Stock without product"


# Signal Handlers
@receiver(post_save, sender=Stock)
def update_total_stock_on_save(sender, instance, created, **kwargs):
    product = instance.product
    if product:
        if instance.stock_type == 'IN':
            product.total_stock += instance.quantity
        elif instance.stock_type == 'OUT':
            if product.total_stock >= instance.quantity:
                product.total_stock -= instance.quantity
            else:
                raise ValueError("Not enough stock to fulfill the 'OUT' request.")
        product.save()
