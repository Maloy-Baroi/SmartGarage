from django.urls import path
from App_main import views

app_name = 'App_main'


urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services_views, name='services'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('campaign/', views.campaign_views, name='campaign'),
    path('comment-send/', views.comment_views, name='comment-send'),
    path('user-dashboard/', views.user_dashboard, name='user-dashboard'),
    path('user-booking/', views.user_booking, name='user-booking'),
    path('booking-view/', views.booking_view, name='booking-view'),
    path('profile-view/', views.user_profile_view, name='profile-view'),
    path('update-profile/', views.user_edit_profile_view, name='update-profile'),
    path('parts-n-accessories/', views.parts_and_accessories_view, name='parts-n-accessories'),
    path('parts-n-accessories-single/<int:id>/', views.singleAccessory_view, name='parts-n-accessories-single'),
]

