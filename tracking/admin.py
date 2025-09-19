from django.contrib import admin
# from django.contrib.gis.admin import GISModelAdmin
from .models import BusStop, Bus, Route, RouteStop, BusRoute, Seat
from users.models import DriverProfile  # Import from users app, not django.contrib

@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):  # Changed from GISModelAdmin
    list_display = ['name', 'code', 'latitude', 'longitude', 'address']
    search_fields = ['name', 'code', 'address']
    list_filter = ['name']

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['bus_number', 'license_plate', 'bus_type', 'total_seats', 'is_active']
    list_filter = ['bus_type', 'is_active']
    search_fields = ['bus_number', 'license_plate']

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'total_distance', 'estimated_duration', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']

@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ['route', 'bus_stop', 'sequence', 'distance_from_previous', 'estimated_time_from_previous']
    list_filter = ['route']
    ordering = ['route', 'sequence']

@admin.register(BusRoute)
class BusRouteAdmin(admin.ModelAdmin):
    list_display = ['bus', 'route', 'driver', 'start_time', 'end_time', 'is_active']
    list_filter = ['is_active', 'route', 'bus', 'driver']
    search_fields = ['bus__bus_number', 'route__name', 'driver__user__username']
    list_editable = ['driver', 'is_active']  # Allow quick editing
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "driver":
            # Only show drivers who are verified
            kwargs["queryset"] = DriverProfile.objects.filter(is_verified=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['bus', 'seat_number', 'is_available']
    list_filter = ['bus', 'is_available']
    ordering = ['bus', 'seat_number']