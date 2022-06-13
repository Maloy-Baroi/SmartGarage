from django.contrib import admin
from App_auth.models import ProfileModel, AddressModel


# Register your models here.
admin.site.register(AddressModel)
admin.site.register(ProfileModel)
