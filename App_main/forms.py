from django import forms
from App_main.models import *


class BookingModelForm(forms.ModelForm):
    booking_date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    contact_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Contact Number'}))

    class Meta:
        model = BookingModel
        exclude = ['user', 'service_name', 'Total_cost', 'status', 'additional_services']


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = CommentOnCampaign
        exclude = ['special_brands']


class CampaignModelForm(forms.ModelForm):
    class Meta:
        model = CampaignModel
        fields = "__all__"


class ServicesModelForm(forms.ModelForm):
    class Meta:
        model = ServicesModel
        exclude = ['details']


class ServicesUpdateModelForm(forms.ModelForm):
    class Meta:
        model = ServicesModel
        exclude = ['name', 'details']


class GalleryModelForm(forms.ModelForm):
    class Meta:
        model = GalleryModel
        fields = '__all__'
