from django.urls import path
from App_admin import views

app_name = 'App_admin'

urlpatterns = [
    path('admin-login-system/', views.admin_login_system, name='admin-login-system'),
    path('', views.admin_dashboard, name='admin-dashboard'),
    path('all-users/', views.allUsers, name='all-users'),
    path('delete-user/<int:delete_id>/', views.delete_user, name='delete-user'),
    path('create-user/', views.create_user_by_admin, name='create-user'),
    path('all-profile-view/', views.allUserProfile, name='all-profile-view'),
    path('create-userProfile-by-admin', views.create_userProfile_by_admin, name='create-userProfile-by-admin'),
    path('single-user-profile/<str:username>/', views.single_user_profile_showcase, name='single-user-profile'),
    path('admin-booking-view/', views.admin_booking_view, name='admin-booking-view'),
    path('update-booking-status/', views.update_booking_status,
         name='update-booking-status'),
    path('admin-campaign-view/', views.admin_campaign_view, name='admin-campaign-view'),
    path('admin-comment-view/', views.admin_comment_view, name='admin-comment-view'),
    path('admin-service-view/', views.admin_service_view, name='admin-service-view'),
    path('admin-service-update-view/<int:pk>/', views.admin_service_update_view, name='admin-service-update-view'),
    path('admin-service-update-status-view/', views.admin_service_update_status_view, name='admin-service-update-status-view'),
    path('admin-gallery-view/', views.admin_gallery_view, name='admin-gallery-view'),
    path('admin-galleryImage-delete-view/<int:deleteID>/', views.admin_galleryImage_delete_view,
         name='admin-galleryImage-delete-view'),
    path('admin-group-view/', views.admin_group_view, name='admin-group-view'),
    path('admin-group-add-view/', views.admin_group_add_view, name='admin-group-add-view'),
    path('admin-group-delete-view/<str:name>/', views.admin_group_delete_view, name='admin-group-delete-view'),
]
