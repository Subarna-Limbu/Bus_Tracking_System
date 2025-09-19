from django.contrib import admin
from .models import Booking, PickupRequest, BusDisruption

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'passenger', 'bus_route', 'travel_date', 'status', 'fare']
    list_filter = ['status', 'travel_date', 'bus_route']
    search_fields = ['passenger__user__username', 'bus_route__bus__bus_number']
    readonly_fields = ['booking_date']

@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'passenger', 'bus_route', 'pickup_stop', 'status', 'requested_time']
    list_filter = ['status', 'requested_time']
    search_fields = ['passenger__user__username', 'bus_route__bus__bus_number']

@admin.register(BusDisruption)
class BusDisruptionAdmin(admin.ModelAdmin):
    list_display = ['bus_route', 'disruption_type', 'start_time', 'is_resolved']
    list_filter = ['disruption_type', 'is_resolved', 'start_time']
    search_fields = ['bus_route__bus__bus_number', 'description']