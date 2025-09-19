from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser, DriverProfile

# Keep these for admin compatibility
class CustomUserCreationForm(UserCreationForm):
    USER_TYPES = (
        ('passenger', 'Passenger'),
        ('driver', 'Driver'),
    )
    
    user_type = forms.ChoiceField(choices=USER_TYPES)
    phone = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'phone')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'phone')

# Your new forms
class PassengerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'passenger'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        
        if commit:
            user.save()
        return user

class DriverRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    license_number = forms.CharField(max_length=50, required=True)
    years_experience = forms.IntegerField(required=True, min_value=0)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'license_number', 'years_experience', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'driver'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        
        if commit:
            user.save()
            # Create driver profile
            DriverProfile.objects.create(
                user=user,
                license_number=self.cleaned_data['license_number'],
                years_experience=self.cleaned_data['years_experience']
            )
        return user

class DriverAuthenticationForm(AuthenticationForm):
    license_number = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Driver License Number'})
    )
    
    def clean(self):
        super().clean()
        
        username = self.cleaned_data.get('username')
        license_number = self.cleaned_data.get('license_number')
        
        if username and license_number:
            try:
                user = CustomUser.objects.get(username=username)
                if user.user_type == 'driver':
                    try:
                        driver_profile = user.driverprofile
                        if driver_profile.license_number != license_number:
                            raise forms.ValidationError("Invalid license number for this driver.")
                    except DriverProfile.DoesNotExist:
                        raise forms.ValidationError("Driver profile not found.")
            except CustomUser.DoesNotExist:
                pass
        
        return self.cleaned_data