from django.urls import path
from App_auth.views import *

app_name = 'App_auth'

urlpatterns = [
    path('register/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
]
