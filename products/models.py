from django.db import models
from django.conf import  settings
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    description =models.TextField()
    image= models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField()
    is_promoted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Promotion(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE,related_name='promotion')
    discount_percentage = models.DecimalField(max_digits=5,decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Promotion for {self.product.name}"