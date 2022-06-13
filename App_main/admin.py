from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ServicesModel)
admin.site.register(BookingModel)
admin.site.register(CampaignModel)
admin.site.register(CommentOnCampaign)
admin.site.register(GalleryModel)
admin.site.register(Parts_n_Accessories_Model)

