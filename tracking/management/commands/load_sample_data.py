from django.core.management.base import BaseCommand
from tracking.models import BusStop, Bus, Route, RouteStop, Seat
from users.models import CustomUser, DriverProfile
import random
from datetime import time

class Command(BaseCommand):
    help = 'Load sample data for the bus tracking system'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Loading sample data...')
        
        # Create sample bus stops around Kathmandu (using lat/long instead of Point)
        stops_data = [
            {'name': 'Central Bus Station', 'code': 'CBS', 'latitude': 27.7172, 'longitude': 85.3188},
            {'name': 'Ratna Park', 'code': 'RTPK', 'latitude': 27.7056, 'longitude': 85.3160},
            {'name': 'New Road', 'code': 'NRD', 'latitude': 27.7043, 'longitude': 85.3105},
            {'name': 'Buspark', 'code': 'BSPK', 'latitude': 27.6965, 'longitude': 85.3124},
            {'name': 'Kalimati', 'code': 'KLM', 'latitude': 27.6984, 'longitude': 85.3028},
            {'name': 'Kalanki', 'code': 'KLK', 'latitude': 27.6934, 'longitude': 85.2811},
            {'name': 'Swayambhu', 'code': 'SWB', 'latitude': 27.7148, 'longitude': 85.2842},
            {'name': 'Gongabu', 'code': 'GGB', 'latitude': 27.7326, 'longitude': 85.3205},
            {'name': 'Koteshwor', 'code': 'KTS', 'latitude': 27.6785, 'longitude': 85.3456},
            {'name': 'Boudha', 'code': 'BDA', 'latitude': 27.7212, 'longitude': 85.3620},
        ]
        
        bus_stops = []
        for stop_data in stops_data:
            stop, created = BusStop.objects.get_or_create(
                code=stop_data['code'],
                defaults={
                    'name': stop_data['name'],
                    'latitude': stop_data['latitude'],
                    'longitude': stop_data['longitude'],
                    'address': f"{stop_data['name']}, Kathmandu"
                }
            )
            bus_stops.append(stop)
        
        self.stdout.write(f'Created {len(bus_stops)} bus stops')
        
        # Create sample buses
        buses_data = [
    {'bus_number': 'B001', 'license_plate': 'BA 101 PA', 'bus_type': 'standard', 'total_seats': 35, 'capacity': 40},
    {'bus_number': 'B002', 'license_plate': 'BA 102 PA', 'bus_type': 'deluxe', 'total_seats': 30, 'capacity': 35},
    {'bus_number': 'B003', 'license_plate': 'BA 103 PA', 'bus_type': 'ac', 'total_seats': 25, 'capacity': 30},
    {'bus_number': 'B004', 'license_plate': 'BA 104 PA', 'bus_type': 'standard', 'total_seats': 35, 'capacity': 40},
    {'bus_number': 'B005', 'license_plate': 'BA 105 PA', 'bus_type': 'deluxe', 'total_seats': 30, 'capacity': 35},
]
        
        buses = []
        for bus_data in buses_data:
            bus, created = Bus.objects.get_or_create(
                bus_number=bus_data['bus_number'],
                defaults=bus_data
            )
            buses.append(bus)
            
            # Create seats for each bus
            for i in range(1, bus.total_seats + 1):
                Seat.objects.get_or_create(
                    bus=bus,
                    seat_number=str(i),
                    defaults={'is_available': True}
                )
        
        self.stdout.write(f'Created {len(buses)} buses with seats')
        
        # Create sample routes
        routes_data = [
            {'name': 'Ring Road East', 'code': 'RRE', 'total_distance': 25.5, 'estimated_duration': 90},
            {'name': 'Ring Road West', 'code': 'RRW', 'total_distance': 23.8, 'estimated_duration': 85},
            {'name': 'City Center Loop', 'code': 'CCL', 'total_distance': 15.2, 'estimated_duration': 60},
            {'name': 'Valley Express', 'code': 'VEX', 'total_distance': 30.0, 'estimated_duration': 120},
        ]
        
        routes = []
        for route_data in routes_data:
            route, created = Route.objects.get_or_create(
                code=route_data['code'],
                defaults=route_data
            )
            routes.append(route)
        
        self.stdout.write(f'Created {len(routes)} routes')
        
        # Create route stops for each route
        route_stop_sequences = {
            'RRE': ['CBS', 'KTS', 'BDA', 'GGB', 'CBS'],
            'RRW': ['CBS', 'SWB', 'KLK', 'KLM', 'CBS'],
            'CCL': ['CBS', 'RTPK', 'NRD', 'BSPK', 'CBS'],
            'VEX': ['CBS', 'KTS', 'BDA', 'SWB', 'KLK', 'CBS'],
        }
        
        for route in routes:
            stop_codes = route_stop_sequences.get(route.code, [])
            for seq, stop_code in enumerate(stop_codes, 1):
                try:
                    bus_stop = BusStop.objects.get(code=stop_code)
                    RouteStop.objects.get_or_create(
                        route=route,
                        bus_stop=bus_stop,
                        sequence=seq,
                        defaults={
                            'distance_from_previous': random.uniform(2.0, 8.0),
                            'estimated_time_from_previous': random.randint(5, 20)
                        }
                    )
                except BusStop.DoesNotExist:
                    continue
        
        self.stdout.write('Created route stop sequences')
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))