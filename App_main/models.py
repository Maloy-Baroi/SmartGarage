from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from io import BytesIO
from django.core.files import File


# Create your models here.
class ServicesModel(models.Model):
    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    details = models.TextField()
    logo = models.ImageField(upload_to='service_logo/', verbose_name=_("service_logo"))
    service_details_image = models.ImageField(upload_to='service_details_image/',
                                              verbose_name=_("service_details_image"))
    status = models.BooleanField(default=True)

    # def save(self, *args, **kwargs):
    #     new_logo = compress(self.logo)
    #     self.logo = new_logo
    #     new_service_image = compress(self.service_details_image)
    #     self.service_details_image = new_service_image
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


service_type_choice_box = (
    ('Home Service', 'Home Service'),
    ('Go to Workshop', 'Go to Workshop'),
)


class BookingModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Booking_user')
    location = models.CharField(max_length=200)
    bike_type = models.CharField(max_length=200)
    service_name = models.ForeignKey(ServicesModel, on_delete=models.CASCADE, related_name='service_name')
    service_type = models.CharField(choices=service_type_choice_box, max_length=50)
    contact_number = models.CharField(max_length=20)
    booking_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now=True)
    additional_services = models.TextField()
    Total_cost = models.IntegerField(blank=True)
    booking_status = (
        ('Service Processing', 'Service Processing'),
        ('Service Accepted', 'Service Accepted'),
        ('Service Confirmed', 'Service Confirmed'),
        ('Service Provided', 'Service Provided'),
        ('Service Rejected', 'Service Rejected'),
    )
    status = models.CharField(choices=booking_status, max_length=20, default='Service Processing')


class CampaignModel(models.Model):
    cam_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='campaign_uploads/')
    details = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.cam_title}"


class CommentOnCampaign(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    special_brands = models.TextField()
    comment = models.TextField()


class GalleryModel(models.Model):
    image = models.ImageField(upload_to='gallery_image/')
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100)
    details = models.TextField()


class Parts_n_Accessories_Model(models.Model):
    name = models.CharField(max_length=100)
    specifications = models.TextField()
    type = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    product_image = models.ImageField(upload_to='productImage/')

