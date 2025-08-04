from django.db import models
from django.conf import  settings
from products.models import Product
# Create your models here.


class BasketItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def total_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('in_transport', 'In Transport'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refund_requested', 'Refund Requested'),
        ('refunded', 'Refunded'),
        ('awaiting_quantity', 'Awaiting Quantity'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20,choices=ORDER_STATUS_CHOICES,default='pending')
    transport_fee = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    def total(self):
        return sum(item.total_price() for item in self.items.all())
    def __str__(self):
        return f"Order #{self.pk} by {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.quantity * self.product.price
