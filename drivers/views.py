from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tracking.models import BusRoute
from notifications.models import Notification

@login_required
def driver_dashboard(request):
    """Driver dashboard with notifications"""
    # Check if user is a driver
    if not hasattr(request.user, 'driverprofile'):
        return redirect('user_home')
    
    # Get assigned bus route
    assigned_bus = BusRoute.objects.filter(driver=request.user.driverprofile, is_active=True).first()
    
    # Get notifications
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:5]
    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    
    # Get today's stats
    today_bookings = 8  # Placeholder
    available_seats = assigned_bus.bus.seats.filter(is_available=True).count() if assigned_bus else 0
    
    return render(request, 'driver_dashboard.html', {
        'assigned_bus': assigned_bus,
        'recent_notifications': notifications,
        'unread_count': unread_count,
        'today_bookings': today_bookings,
        'available_seats': available_seats,
    })

@login_required
def driver_notifications(request):
    """Driver notifications page"""
    if not hasattr(request.user, 'driverprofile'):
        return redirect('user_home')
    
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    
    # Mark all as read when viewing notifications page
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    
    return render(request, 'driver_notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })