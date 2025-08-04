from django.db import models

# Create your models here.
class HomepageContent(models.Model):
    description = models.TextField(default="Welcome to OnlineMag!")

    def __str__(self):
        return "Homepage Description"



class TransportSettings(models.Model):
    threshold = models.DecimalField(max_digits=10,decimal_places=2, default=50.00)
    fee = models.DecimalField(max_digits=10,decimal_places=2,default=5.00)

    def __str__(self):
        return "Transport Settings"


