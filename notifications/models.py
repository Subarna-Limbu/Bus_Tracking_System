from django.db import models
from django.contrib.auth import get_user_model

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('pickup_request', 'Pickup Request'),
        ('booking_confirmation', 'Booking Confirmation'),
        ('system_alert', 'System Alert'),
    )
    
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type} - {self.recipient.username}"