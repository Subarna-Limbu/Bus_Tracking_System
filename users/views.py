from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .forms import PassengerRegistrationForm, DriverRegistrationForm, DriverAuthenticationForm
from .models import PassengerProfile, DriverProfile
from django.utils import timezone

def register(request):
    user_type = request.GET.get('type', 'passenger')
    
    if request.method == 'POST':
        if user_type == 'driver':
            form = DriverRegistrationForm(request.POST)
        else:
            form = PassengerRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            # Create passenger profile if needed
            if user.user_type == 'passenger':
                PassengerProfile.objects.create(user=user)
            
            # Redirect to login page with success message
            login_url = reverse('login') + f'?type={user_type}&success=1'
            return redirect(login_url)
    else:
        if user_type == 'driver':
            form = DriverRegistrationForm()
        else:
            form = PassengerRegistrationForm()
    
    return render(request, f'registration/{user_type}_register.html', {
        'form': form,
        'user_type': user_type
    })

def custom_login(request):
    user_type = request.GET.get('type', 'passenger')
    success = request.GET.get('success', False)
    
    if user_type == 'driver':
        form_class = DriverAuthenticationForm
        template_name = 'registration/driver_login.html'
    else:
        form_class = AuthenticationForm
        template_name = 'registration/login.html'
    
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = form_class()
    
    return render(request, template_name, {
        'form': form, 
        'user_type': user_type,
        'success': success
    })


@login_required
def dashboard(request):
    """Main dashboard redirect"""
    if request.user.user_type == 'passenger':
        return redirect('user_home')
    elif request.user.user_type == 'driver':
        # Check if driver is verified
        try:
            if request.user.driverprofile.is_verified:
                return redirect('driver_dashboard')
            else:
                return redirect('driver_pending')
        except:
            return redirect('driver_pending')
    else:
        return redirect('admin_dashboard')
    
@login_required
def user_home(request):
    """User home page with route selection"""
    from tracking.models import BusStop
    
    bus_stops = BusStop.objects.all()
    return render(request, 'user_home.html', {
        'bus_stops': bus_stops,
    })
@login_required
def profile_dashboard(request):
    """Profile dashboard for passengers"""
    return render(request, 'profile_dashboard.html')

@login_required
def passenger_dashboard(request):
    """Keep this for future use if needed"""
    return render(request, 'dashboard_passenger.html')

@login_required
def passenger_dashboard(request):
    return render(request, 'dashboard_passenger.html')

@login_required
def driver_dashboard(request):
    """Driver dashboard - only accessible if verified"""
    try:
        driver_profile = request.user.driverprofile
        if not driver_profile.is_verified:
            return redirect('driver_pending')
    except DriverProfile.DoesNotExist:
        return redirect('driver_pending')
    
    return render(request, 'dashboard_driver.html')

@login_required
def driver_pending(request):
    """Driver pending verification page"""
    try:
        driver_profile = request.user.driverprofile
    except DriverProfile.DoesNotExist:
        # If no driver profile exists, create one (fallback)
        driver_profile = DriverProfile.objects.create(
            user=request.user,
            license_number="Not provided",
            years_experience=0
        )
    
    return render(request, 'driver_first.html', {
        'driver_profile': driver_profile
    })
    
@login_required
def admin_dashboard(request):
    return render(request, 'dashboard_admin.html')

def save(self, commit=True):
    user = super().save(commit=False)
    user.user_type = 'driver'
    user.first_name = self.cleaned_data['first_name']
    user.last_name = self.cleaned_data['last_name']
    user.email = self.cleaned_data['email']
    user.phone = self.cleaned_data['phone']
    
    if commit:
        user.save()
        # Create driver profile with is_verified=False
        DriverProfile.objects.create(
            user=user,
            license_number=self.cleaned_data['license_number'],
            years_experience=self.cleaned_data['years_experience'],
            is_verified=False  # Default to not verified
        )
    return user