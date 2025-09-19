from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import BusStop, Bus, Route, BusRoute, Seat
from booking.models import Booking
from datetime import datetime
import json
from django.contrib.auth import get_user_model
from notifications.models import Notification


@login_required
def map_view(request):
    """Main map view for stop selection"""
    bus_stops = BusStop.objects.all()
    routes = Route.objects.filter(is_active=True)
    
    # Convert bus stops to GeoJSON format for Leaflet
    bus_stops_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [stop.longitude, stop.latitude],
                },
                "properties": {
                    "id": stop.id,
                    "name": stop.name,
                    "code": stop.code,
                    "address": stop.address,
                }
            } for stop in bus_stops
        ]
    }
    
    return render(request, 'tracking/map.html', {
        'bus_stops': bus_stops,
        'bus_stops_geojson': json.dumps(bus_stops_geojson),
        'routes': routes,
    })

@login_required
def find_routes(request):
    """Find routes between two stops"""
    if request.method == 'POST':
        pickup_stop_id = request.POST.get('pickup_stop')
        destination_stop_id = request.POST.get('destination_stop')
        
        try:
            pickup_stop = BusStop.objects.get(id=pickup_stop_id)
            destination_stop = BusStop.objects.get(id=destination_stop_id)
            
            return render(request, 'tracking/route_results.html', {
                'pickup_stop': pickup_stop,
                'destination_stop': destination_stop,
            })
        except BusStop.DoesNotExist:
            return render(request, 'tracking/map.html', {
                'error': 'Invalid stop selection',
                'bus_stops': BusStop.objects.all(),
                'routes': Route.objects.filter(is_active=True),
                'bus_stops_geojson': json.dumps([]),
            })
    
    return redirect('tracking:map_view')

@login_required
def find_buses(request):
    """Find available buses between two stops"""
    if request.method == 'POST':
        start_stop_id = request.POST.get('start_stop')
        end_stop_id = request.POST.get('end_stop')
        
        try:
            start_stop = BusStop.objects.get(id=start_stop_id)
            end_stop = BusStop.objects.get(id=end_stop_id)
            
            # For Phase 3: Show all active buses
            available_buses = Bus.objects.filter(is_active=True)[:3]
            
            # Return JSON response for AJAX handling
            buses_data = []
            for bus in available_buses:
                available_seats = bus.seats.filter(is_available=True).count()
                buses_data.append({
                    'id': bus.id,
                    'number': bus.bus_number,
                    'route': bus.bus_routes.first().route.name if bus.bus_routes.exists() else 'No Route',
                    'available_seats': available_seats,
                    'total_seats': bus.total_seats
                })
            
            return JsonResponse({'buses': buses_data})
            
        except (BusStop.DoesNotExist, ValueError):
            return JsonResponse({'error': 'Invalid stop selection'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def bus_details(request, bus_id):
    """Show bus details, route map, and seat selection"""
    bus = get_object_or_404(Bus, id=bus_id)
    start_stop_id = request.GET.get('start_stop')
    end_stop_id = request.GET.get('end_stop')
    travel_date = request.GET.get('travel_date')
    
    try:
        start_stop = BusStop.objects.get(id=start_stop_id)
        end_stop = BusStop.objects.get(id=end_stop_id)
    except BusStop.DoesNotExist:
        return redirect('user_home')
    
    # Get seats for this bus
    seats = Seat.objects.filter(bus=bus).order_by('seat_number')
    
    # Get sample route for this bus
    sample_route = Route.objects.filter(bus_routes__bus=bus).first()
    
    return render(request, 'tracking/bus_details.html', {
        'bus': bus,
        'start_stop': start_stop,
        'end_stop': end_stop,
        'travel_date': travel_date,
        'seats': seats,
        'sample_route': sample_route,
    })

@login_required
def book_seat(request):
    """Handle seat booking with confirmation"""
    if request.method == 'POST':
        bus_id = request.POST.get('bus_id')
        seat_id = request.POST.get('seat_id')
        start_stop_id = request.POST.get('start_stop_id')
        end_stop_id = request.POST.get('end_stop_id')
        travel_date = request.POST.get('travel_date')
        
        try:
            bus = Bus.objects.get(id=bus_id)
            seat = Seat.objects.get(id=seat_id, bus=bus)
            start_stop = BusStop.objects.get(id=start_stop_id)
            end_stop = BusStop.objects.get(id=end_stop_id)
            
            # Check if seat is available
            if not seat.is_available:
                return JsonResponse({'success': False, 'message': 'Seat is already booked'})
            
            # Get bus route and driver
            bus_route = BusRoute.objects.filter(bus=bus).first()
            
            # Create booking
            booking = Booking.objects.create(
                passenger=request.user.passengerprofile,
                bus_route=bus_route,
                seat=seat,
                pickup_stop=start_stop,
                dropoff_stop=end_stop,
                travel_date=travel_date,
                fare=50.00,
                status='confirmed'
            )
            
            # Mark seat as unavailable
            seat.is_available = False
            seat.save()
            
            # Send notification to driver if assigned
            if bus_route and bus_route.driver:
                driver_user = bus_route.driver.user
                Notification.objects.create(
                    recipient=driver_user,
                    notification_type='pickup_request',
                    title='New Pickup Request',
                    message=f'Passenger {request.user.username} has booked seat {seat.seat_number} on bus {bus.bus_number} from {start_stop.name} to {end_stop.name}',
                    related_object_id=booking.id,
                    related_content_type='booking'
                )
            
            # Send confirmation to passenger
            Notification.objects.create(
                recipient=request.user,
                notification_type='booking_confirmation',
                title='Booking Confirmed',
                message=f'Your seat {seat.seat_number} on bus {bus.bus_number} has been confirmed. Driver has been notified.',
                related_object_id=booking.id,
                related_content_type='booking'
            )
            
            return JsonResponse({
                'success': True, 
                'message': f'Seat {seat.seat_number} booked successfully!',
                'booking_id': booking.id
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})
@login_required
def bus_map(request):
    """Show bus map and seat selection"""
    bus_id = request.GET.get('bus_id')
    start_stop_id = request.GET.get('start_stop')
    end_stop_id = request.GET.get('end_stop')
    
    try:
        bus = Bus.objects.get(id=bus_id)
        start_stop = BusStop.objects.get(id=start_stop_id)
        end_stop = BusStop.objects.get(id=end_stop_id)
        
        # Get bus route (simplified for demo)
        bus_route = BusRoute.objects.filter(bus=bus).first()
        
        # Get seats for this bus
        seats = Seat.objects.filter(bus=bus).order_by('seat_number')
        
        # Get all bus stops for the map
        all_bus_stops = BusStop.objects.all()
        
        # Create GeoJSON for all bus stops
        bus_stops_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [stop.longitude, stop.latitude],
                    },
                    "properties": {
                        "id": stop.id,
                        "name": stop.name,
                        "code": stop.code,
                    }
                } for stop in all_bus_stops
            ]
        }
        
        return render(request, 'tracking/bus_map.html', {
            'bus': bus,
            'start_stop': start_stop,
            'end_stop': end_stop,
            'bus_route': bus_route,
            'seats': seats,
            'bus_stops_geojson': json.dumps(bus_stops_geojson),
            'all_bus_stops': all_bus_stops,
        })
        
    except (Bus.DoesNotExist, BusStop.DoesNotExist):
        return redirect('user_home')