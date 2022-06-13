import json

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from itertools import chain
from App_auth.forms import SignupForm, ProfileModelForm, AddressModelForm
from App_auth.models import ProfileModel, AddressModel
from App_main.models import *
from App_main.forms import *


# Create your views here.
def loginForm_():
    loginForm = AuthenticationForm()
    loginForm.fields['username'].widget.attrs['placeholder'] = "Username"
    loginForm.fields['password'].widget.attrs['placeholder'] = "Password"
    return loginForm


def totalCostForServices(thisList, total_cost):
    if len(thisList) == 0:
        return total_cost
    else:
        if ServicesModel.objects.filter(name=thisList[0]).exists():
            total_cost += ServicesModel.objects.get(name=thisList[0]).cost
        thisList.remove(thisList[0])
        return totalCostForServices(thisList, total_cost)


def home(request):
    services = ServicesModel.objects.filter(status=True)
    bookingForm = BookingModelForm()
    loginForm = AuthenticationForm()
    loginForm.fields['username'].widget.attrs['placeholder'] = "Phone Number"
    loginForm.fields['password'].widget.attrs['placeholder'] = "Password"
    signupForm = SignupForm()
    if request.method == 'POST':
        # Total Cost and additional Services
        additionalList = request.POST.getlist('additional-services')
        mainServ = request.POST.get('service')
        additionalList.remove(mainServ)
        mainService = services.get(name=mainServ)
        # End
        bookingForm = BookingModelForm(request.POST)
        if bookingForm.is_valid():
            thisForm = bookingForm.save(commit=False)
            thisForm.service_type = mainService
            thisForm.additional_services = ", ".join(additionalList)
            thisForm.user = request.user
            thisForm.Total_cost = totalCostForServices(additionalList, mainService.cost)
            thisForm.save()

            return HttpResponseRedirect(reverse('App_main:home'))

    content = {
        'services': services,
        'bookingForm': bookingForm,
        'loginForm': loginForm,
        'signupForm': signupForm,
    }
    return render(request, 'App_main/home.html', context=content)


def services_views(request):
    services = ServicesModel.objects.filter(status=True)
    content = {
        'services': services,
        'loginForm': loginForm_(),
    }
    return render(request, 'App_main/service.html', context=content)


def campaign_views(request):
    content = {
        'loginForm': loginForm_(),
    }
    return render(request, 'App_main/campaign.html', context=content)


@login_required
def booking_view(request):
    bookingForm = BookingModelForm()
    services = ServicesModel.objects.all()
    if request.method == 'POST':
        # Total Cost and additional Services
        additionalList = request.POST.getlist('additional-services')
        mainServ = request.POST.get('main-service')
        if mainServ in additionalList:
            additionalList.remove(mainServ)
        mainService = services.get(name=mainServ)
        # End
        bookingForm = BookingModelForm(data=request.POST)
        if bookingForm.is_valid():
            thisForm = bookingForm.save(commit=False)
            thisForm.service_name = mainService
            thisForm.additional_services = ", ".join(additionalList)
            thisForm.user = request.user
            all_cost = totalCostForServices(additionalList, mainService.cost)
            thisForm.Total_cost = all_cost
            thisForm.save()
            return HttpResponseRedirect(reverse('App_main:user-booking'))
    content = {
        'bookingForm': bookingForm,
        'services': services,
    }
    return render(request, 'App_main/bookings.html', context=content)


def comment_views(request):
    if request.method == 'POST':
        form = CommentModelForm(data=request.POST)
        if form.is_valid():
            thisForm = form.save(commit=False)
            thisForm.special_brands = request.POST.getlist('brands')
            thisForm.save()
            return HttpResponseRedirect(reverse('App_main:campaign'))


@login_required
def user_dashboard(request):
    return render(request, 'App_main/dashboard.html')


@login_required
def user_booking(request):
    myBookings = BookingModel.objects.filter(user=request.user)
    requested = BookingModel.objects.filter(user=request.user, status="Service Processing")
    accepted = BookingModel.objects.filter(user=request.user, status="Service Accepted")
    confirmed = BookingModel.objects.filter(user=request.user, status="Service Confirmed")
    ready = BookingModel.objects.filter(user=request.user, status="Service Provided")
    rejected = BookingModel.objects.filter(user=request.user, status="Service Rejected")

    content = {
        'requested': requested,
        'accepted': accepted,
        'confirmed': confirmed,
        'ready': ready,
        'rejected': rejected,
        'ongoing': confirmed,
    }
    return render(request, 'App_main/user_bookings_view.html', context=content)


@login_required
def user_profile_view(request):
    try:
        profile = ProfileModel.objects.get(user=request.user)
    except:
        profile = None
    content = {
        'profile': profile
    }
    return render(request, 'App_main/profile_view.html', context=content)


@login_required
def user_edit_profile_view(request):
    try:
        profileInstance = ProfileModel.objects.get(user=request.user)
    except:
        profileInstance = None
        address = None
    ProfileForm = ProfileModelForm(instance=profileInstance)
    if request.method == 'POST':
        ProfileForm = ProfileModelForm(request.POST, request.FILES)
        if ProfileForm.is_valid():
            thisProfile = ProfileForm.save(commit=False)
            thisProfile.user = request.user
            thisProfile.save()
    content = {
        'ProfileForm': ProfileForm,
    }
    return render(request, 'App_main/update_user_profile.html', context=content)


def parts_and_accessories_view(request):
    parts = Parts_n_Accessories_Model.objects.all()
    content = {
        'parts_n_accessories': parts,
    }
    return render(request, 'App_main/parts_and_accessories.html', context=content)


def singleAccessory_view(request, id):
    part = Parts_n_Accessories_Model.objects.get(id=id)
    content = {
        'part': part,
    }
    return render(request, 'App_main/parts_and_accessories_single.html', context=content)


def gallery_view(request):
    galleryObj = GalleryModel.objects.all()
    content = {
        'galleryObj': galleryObj,
    }
    return render(request, 'App_main/gallery.html', context=content)

# # API View
# @permission_classes([AllowAny, ])
# @api_view(['GET', 'POST', ])
# def homeAPI(request):
#     if request.method == 'GET':
#         service = ServicesModel.objects.filter(status=True)
#         serializer = ServicesModelSerializer(service, many=True)
#         return Response(serializer.data)


# class HomeAPIView(ListCreateAPIView):
#     permission_classes = [IsAuthenticated, ]
#     queryset = BookingModel.objects.all()
#     serializer_class = BookingModelSerializer

#     def perform_create(self, serializer):
#         service = self.request.data['service']
#         sType = ServicesModel.objects.get(name=service)
#         add_services = str(self.request.data['additional-services'])
#         add_services = add_services.split(", ")
#         newList, total_cost = totalCostForServices(add_services, sType.cost)
#         _additional_services = "".join(newList)
#         return serializer.save(user=self.request.user, service_type=sType, Total_cost=total_cost,
#                                additional_services=_additional_services)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = BookingModelSerializerFull(queryset, many=True)
#         return Response(serializer.data)


# class ServicesAPIView(ListAPIView):
#     permission_classes = [AllowAny, ]
#     queryset = ServicesModel.objects.all()
#     serializer_class = ServicesModelSerializer

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = ServicesModelSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def get_queryset(self):
#         queryset = ServicesModel.objects.filter(status=True)
#         return queryset


# class Comment_n_campaign_APIView(ListCreateAPIView):
#     permission_classes = [AllowAny, ]
#     queryset = CommentOnCampaign.objects.all()
#     serializer_class = CommentModelSerializer

#     def perform_create(self, serializer):
#         return serializer.save()

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = CampaignModelSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def get_queryset(self):
#         queryset = CampaignModel.objects.all()
#         return queryset
