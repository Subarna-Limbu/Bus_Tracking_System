from django.urls import path
from . import views

app_name = 'drivers'

urlpatterns = [
    path('dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('notifications/', views.driver_notifications, name='driver_notifications'),
]