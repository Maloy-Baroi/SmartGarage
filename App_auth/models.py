from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.
class AddressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_address')
    House_no = models.CharField(max_length=50)
    Area = models.CharField(max_length=100)
    Thana = models.CharField(max_length=100)
    Pin_code = models.CharField(max_length=6)
    City = models.CharField(max_length=100)


class ProfileModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200, default=None)
    photo = models.ImageField(upload_to='customer_image')

