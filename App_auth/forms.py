from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from App_auth.models import ProfileModel, AddressModel


class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Phone Number"}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Phone Number"


class AddressModelForm(forms.ModelForm):
    class Meta:
        model = AddressModel
        exclude = ['user']


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        exclude = ['user',]

