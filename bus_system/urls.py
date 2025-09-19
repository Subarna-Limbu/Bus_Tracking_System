"""
URL configuration for bus_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from users import views
from django.contrib.auth import views as auth_views
from users import views as user_views
from tracking import views as tracking_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('passenger-dashboard/', views.passenger_dashboard, name='passenger_dashboard'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('user-home/', views.user_home, name='user_home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('profile/', views.profile_dashboard, name='profile_dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('driver-pending/', views.driver_pending, name='driver_pending'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('tracking/', include('tracking.urls')),
     path('bus-map/', tracking_views.bus_map, name='bus_map'),
    path('find-buses/', tracking_views.find_buses, name='find_buses'),
    path('bus/<int:bus_id>/', tracking_views.bus_details, name='bus_details'),
    path('book-seat/', tracking_views.book_seat, name='book_seat'),
     path('', user_views.user_home, name='user_home'),
     path('driver/', include('drivers.urls')),
    
]