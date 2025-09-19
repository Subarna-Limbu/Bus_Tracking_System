from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('map/', views.map_view, name='map_view'),
    path('find-routes/', views.find_routes, name='find_routes'),
    path('find-buses/', views.find_buses, name='find_buses'),
    path('bus/<int:bus_id>/', views.bus_details, name='bus_details'),
    path('book-seat/', views.book_seat, name='book_seat'),
      path('map/', views.bus_map, name='bus_map'),
]