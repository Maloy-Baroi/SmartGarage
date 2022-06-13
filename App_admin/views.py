from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test

from App_auth.forms import AddressModelForm, ProfileModelForm, SignupForm
from App_auth.models import *
from App_main.forms import CampaignModelForm, ServicesModelForm, GalleryModelForm, ServicesUpdateModelForm
from App_main.models import BookingModel, ServicesModel, CommentOnCampaign, CampaignModel, GalleryModel


# Create your views here.
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


def total_client(userList, total):
    if len(userList) == 0:
        return total
    else:
        if is_customer(userList[0]):
            total += 1
        userList.remove(userList[0])
        return total_client(userList, total)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_dashboard(request):
    try:
        profile = ProfileModel.objects.get(user=request.user)
    except:
        profile = None
    total_served_order = BookingModel.objects.filter(status='Service Provided')
    total_pending_order = BookingModel.objects.filter(status='Service Processing')
    total_order = BookingModel.objects.all()
    total_groups = Group.objects.all()
    total_comment = CommentOnCampaign.objects.all()
    all_user = User.objects.all()
    total_user = total_client(list(all_user), 0)
    services = ServicesModel.objects.all()
    content = {
        'profile': profile,
        'total_served_order': total_served_order,
        'total_pending_order': total_pending_order,
        'total_order': total_order,
        'total_group': total_groups,
        'total_comment': total_comment,
        'total_user': total_user,
        'total_services': services,
    }
    return render(request, 'App_admin/dashboard.html', context=content)


def admin_login_system(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=user_email, password=password)
            if user:
                login(request, user)
                if is_admin(user):
                    return HttpResponseRedirect(reverse('App_admin:admin-dashboard'))
                return HttpResponseRedirect(reverse('App_admin:admin-login-system'))
    content = {
        'form': form
    }
    return render(request, 'App_admin/login_page.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def allUsers(request):
    users = User.objects.filter(is_superuser=False)
    content = {
        'users': users
    }
    return render(request, 'App_admin/all_users.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def create_user_by_admin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = User(username=username)
    user.set_password(password)
    user.is_superuser = False
    user.is_active = True
    user.is_staff = False
    user.save()

    return HttpResponseRedirect(reverse('App_admin:all-users'))


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def delete_user(request, delete_id):
    user = User.objects.get(id=delete_id)
    user.delete()
    return HttpResponseRedirect(reverse('App_admin:all-users'))


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def allUserProfile(request):
    profiles = ProfileModel.objects.filter(user__is_superuser=False)
    users = User.objects.filter(is_superuser=False)
    profileForm = ProfileModelForm()
    content = {
        'profiles': profiles,
        'users': users,
        'profileForm': profileForm,
    }
    return render(request, 'App_admin/all_profile.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def create_userProfile_by_admin(request):
    if request.method == 'POST':
        userFor = request.POST.get('user')
        user = User.objects.get(username=userFor)
        profileForm = ProfileModelForm(request.POST, request.FILES)
        if profileForm.is_valid():
            thisProfile = profileForm.save(commit=False)
            thisProfile.user = user
            thisProfile.save()
            return HttpResponseRedirect(reverse('App_admin:all-profile-view'))
    return HttpResponseRedirect(reverse('App_admin:all-profile-view'))


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def single_user_profile_showcase(request, username):
    user = User.objects.get(username=username)
    profile = ProfileModel.objects.get(user=user)
    userForm = SignupForm(instance=user)
    profileForm = ProfileModelForm(instance=profile)
    if request.method == 'POST':
        userForm = SignupForm(request.post, request.files)
        profileForm = ProfileModelForm(request.post)
        if userForm.is_valid() and profileForm.is_valid():
            u = userForm.save()
            this_profile = profileForm.save(commit=False)
            this_profile.user = u
            this_profile.save()
            return HttpResponseRedirect(reverse('App_admin:single-user-profile', kwargs=u.username))
    content = {
        'userForm': userForm,
        'profileForm': profileForm,
    }
    return render(request, 'App_admin/single_user_profile.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_booking_view(request):
    bookings = BookingModel.objects.all()
    content = {
        'bookings': bookings
    }
    return render(request, 'App_admin/admin_booking_view.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def update_booking_status(request):
    if request.method == 'POST':
        bookingID = request.POST.get('bookingID')
        bookingStatus = request.POST.get('status')
        booking = BookingModel.objects.get(id=bookingID)
        booking.status = bookingStatus
        booking.save()
        return HttpResponseRedirect(reverse('App_admin:admin-booking-view'))
    return HttpResponseRedirect(reverse('App_admin:admin-booking-view'))


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_campaign_view(request):
    campaigns = CampaignModel.objects.all()
    add_campaignForm = CampaignModelForm()
    if request.method == 'POST':
        add_campaignForm = CampaignModelForm(data=request.POST)
        if add_campaignForm.is_valid():
            add_campaignForm.save()
    content = {
        'campaigns': campaigns,
        'campForm': add_campaignForm
    }
    return render(request, 'App_admin/admin_campaign_view.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_comment_view(request):
    comments = CommentOnCampaign.objects.all()
    content = {
        'comments': comments
    }
    return render(request, 'App_admin/admin_comment_view.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_service_view(request):
    services = ServicesModel.objects.all()
    serviceForm = ServicesModelForm()
    if request.method == 'POST':
        details = request.POST.get('my-service-content')
        serviceForm = ServicesModelForm(request.POST, request.FILES)
        if serviceForm.is_valid():
            serv = serviceForm.save(commit=False)
            serv.details = details
            serv.save()
            return HttpResponseRedirect(reverse('App_admin:admin-service-view'))
    content = {
        'services': services,
        'serviceForm': serviceForm,
    }
    return render(request, 'App_admin/admin_service_view.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_service_update_view(request, pk):
    serv = ServicesModel.objects.get(id=pk)
    form = ServicesUpdateModelForm(instance=serv)
    if request.method == 'POST':
        details = request.POST.get('my-service-content')
        form = ServicesUpdateModelForm(request.POST, request.FILES, instance=serv)
        if form.is_valid():
            print('is valid')
            # form.save()
            print(details)
            servForm = form.save(commit=False)
            servForm.details = details
            servForm.save()
            return HttpResponseRedirect(reverse('App_admin:admin-service-view'))
    content = {
        'form': form,
        'service': serv,
    }
    return render(request, 'App_admin/admin-service-update-view.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_service_update_status_view(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        servID = request.POST.get('serviceID')
        service = ServicesModel.objects.get(id=servID)
        service.status = status
        service.save()
        return HttpResponseRedirect(reverse('App_admin:admin-service-view'))


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_gallery_view(request):
    gallery = GalleryModel.objects.all()
    galleryForm = GalleryModelForm()
    if request.method == 'POST':
        galleryForm = GalleryModelForm(request.POST, request.FILES)
        if galleryForm.is_valid():
            galleryForm.save()
    content = {
        'galleryImages': gallery,
        'galleryForm': galleryForm,
    }
    return render(request, 'App_admin/admin_gallery_view.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_galleryImage_delete_view(request, deleteID):
    image = GalleryModel.objects.get(id=deleteID)
    image.delete()
    return HttpResponseRedirect(reverse('App_admin:admin-gallery-view'))


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_group_view(request):
    groups = Group.objects.all()
    content = {
        'groups': groups
    }
    return render(request, 'App_admin/admin_groups.html', context=content)


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_group_add_view(request):
    if request.method == 'POST':
        name = request.POST.get('group_name')
        group = Group.objects.create(name=name)
        group.save()
        return HttpResponseRedirect(reverse('App_admin:admin-group-view'))


@login_required(login_url='App_admin:admin-login-system')
@user_passes_test(is_admin)
def admin_group_delete_view(request, name):
    group = Group.objects.get(name=name)
    group.delete()
    return HttpResponseRedirect(reverse('App_admin:admin-group-view'))
