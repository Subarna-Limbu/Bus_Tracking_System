from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .forms import PassengerRegistrationForm, DriverRegistrationForm, DriverAuthenticationForm
from .models import PassengerProfile, DriverProfile

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
    if request.user.user_type == 'passenger':
        return redirect('user_home')  # Redirect to user home instead of passenger dashboard
    elif request.user.user_type == 'driver':
        return redirect('driver_dashboard')
    else:
        return redirect('admin_dashboard')
    
@login_required
def user_home(request):
    """New view for user home page with route selection"""
    return render(request, 'user_home.html')

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
    return render(request, 'dashboard_driver.html')

@login_required
def admin_dashboard(request):
    return render(request, 'dashboard_admin.html')