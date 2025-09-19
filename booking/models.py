from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Booking(models.Model):
    BOOKING_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    passenger = models.ForeignKey('users.PassengerProfile', on_delete=models.CASCADE, related_name='bookings')
    bus_route = models.ForeignKey('tracking.BusRoute', on_delete=models.CASCADE, related_name='bookings')
    seat = models.ForeignKey('tracking.Seat', on_delete=models.CASCADE, related_name='bookings')
    pickup_stop = models.ForeignKey('tracking.BusStop', on_delete=models.CASCADE, related_name='pickups')
    dropoff_stop = models.ForeignKey('tracking.BusStop', on_delete=models.CASCADE, related_name='dropoffs')
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_date = models.DateField()
    status = models.CharField(max_length=10, choices=BOOKING_STATUS, default='pending')
    fare = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"Booking #{self.id} - {self.passenger.user.username}"

class PickupRequest(models.Model):
    REQUEST_STATUS = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )
    
    passenger = models.ForeignKey('users.PassengerProfile', on_delete=models.CASCADE, related_name='pickup_requests')
    bus_route = models.ForeignKey('tracking.BusRoute', on_delete=models.CASCADE, related_name='pickup_requests')
    pickup_stop = models.ForeignKey('tracking.BusStop', on_delete=models.CASCADE)
    requested_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default='pending')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Pickup Request #{self.id} - {self.passenger.user.username}"

class BusDisruption(models.Model):
    DISRUPTION_TYPES = (
        ('accident', 'Accident'),
        ('traffic', 'Heavy Traffic'),
        ('breakdown', 'Bus Breakdown'),
        ('weather', 'Bad Weather'),
        ('other', 'Other'),
    )
    
    bus_route = models.ForeignKey('tracking.BusRoute', on_delete=models.CASCADE, related_name='disruptions')
    disruption_type = models.CharField(max_length=20, choices=DISRUPTION_TYPES)
    description = models.TextField()
    start_time = models.DateTimeField()
    expected_end_time = models.DateTimeField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    reported_by = models.ForeignKey('users.DriverProfile', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Disruption: {self.disruption_type} on {self.bus_route}"