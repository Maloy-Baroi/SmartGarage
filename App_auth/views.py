from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import Group

from App_admin.views import is_customer, is_admin
from App_auth.forms import *


# Create your views here.
def registerView(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            customer_group = Group.objects.get_or_create(name='CUSTOMER')
            customer_group[0].user_set.add(user)
            return HttpResponseRedirect(reverse('App_main:home'))
    return HttpResponseRedirect(reverse('App_main:home'))


def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if is_customer(user):
                    return HttpResponseRedirect(reverse('App_main:home'))
                elif is_admin(user):
                    return HttpResponseRedirect(reverse('App_admin:admin-dashboard'))
                next_view = request.POST.get('next', '/')
                return HttpResponseRedirect(next_view)

    return HttpResponseRedirect(reverse('App_main:home'))


def logoutView(request):
    logout(request)
    next_view = request.POST.get('next', '/')
    return HttpResponseRedirect(next_view)
