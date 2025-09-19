from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('passenger', 'Passenger'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='passenger')
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class PassengerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # favorite_stops = models.ManyToManyField('tracking.BusStop', blank=True)
    
    def __str__(self):
        return f"Passenger: {self.user.username}"

class DriverProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    years_experience = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)  # Add this field
    verification_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Driver: {self.user.username} (Verified: {self.is_verified})"