from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin','Admin'),
        ('owner','Owner'),
        ('user','User')
    )

    picture = models.ImageField(upload_to='profile_pics/',null=True,blank=True)
    phone= models.CharField(max_length=15,blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,default='user')
    objects = UserManager()
    @property
    def is_owner(self):
        return self.role =='owner'
    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
