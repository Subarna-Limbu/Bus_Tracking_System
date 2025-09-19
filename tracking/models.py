from django.db import models

class BusStop(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Bus(models.Model):
    BUS_TYPES = (
        ('standard', 'Standard'),
        ('deluxe', 'Deluxe'),
        ('ac', 'Air Conditioned'),
    )
    
    bus_number = models.CharField(max_length=20, unique=True)
    license_plate = models.CharField(max_length=15, unique=True)
    bus_type = models.CharField(max_length=10, choices=BUS_TYPES, default='standard')
    total_seats = models.IntegerField(default=30)
    capacity = models.IntegerField(help_text="Maximum passenger capacity")  # This field cannot be null!
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.bus_number} - {self.license_plate}"
    BUS_TYPES = (
        ('standard', 'Standard'),
        ('deluxe', 'Deluxe'),
        ('ac', 'Air Conditioned'),
    )
    
    bus_number = models.CharField(max_length=20, unique=True)
    license_plate = models.CharField(max_length=15, unique=True)
    bus_type = models.CharField(max_length=10, choices=BUS_TYPES, default='standard')
    total_seats = models.IntegerField(default=30)
    capacity = models.IntegerField(help_text="Maximum passenger capacity")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.bus_number} - {self.license_plate}"

class Route(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    total_distance = models.FloatField(help_text="Distance in kilometers", default=0)
    estimated_duration = models.IntegerField(help_text="Estimated duration in minutes", default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='route_stops')
    bus_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE)
    sequence = models.IntegerField(help_text="Order of stops in the route")
    distance_from_previous = models.FloatField(help_text="Distance from previous stop in km", default=0)
    estimated_time_from_previous = models.IntegerField(help_text="Time from previous stop in minutes", default=0)
    
    class Meta:
        ordering = ['route', 'sequence']
        unique_together = ['route', 'sequence']
    
    def __str__(self):
        return f"{self.route.name} - Stop {self.sequence}: {self.bus_stop.name}"

class BusRoute(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='bus_routes')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='bus_routes')
    driver = models.ForeignKey('users.DriverProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_routes')
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['bus', 'route', 'start_time']
    
    def __str__(self):
        driver_name = self.driver.user.get_full_name() if self.driver else 'No Driver'
        return f"{self.bus.bus_number} - {self.route.name} - {driver_name}"
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='bus_routes')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='bus_routes')
    driver = models.ForeignKey('users.DriverProfile', on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['bus', 'route', 'start_time']
    
    def __str__(self):
        return f"{self.bus.bus_number} on {self.route.name} at {self.start_time}"

class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['bus', 'seat_number']
    
    def __str__(self):
        return f"{self.bus.bus_number} - Seat {self.seat_number}"