from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PassengerProfile, DriverProfile
from .forms import CustomUserCreationForm, CustomUserChangeForm
from datetime import datetime
from django.utils import timezone

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'user_type', 'phone']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'phone')}),
    )

class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'license_number', 'years_experience', 'is_verified', 'verification_date']
    list_editable = ['is_verified']  # Allow quick verification from list view
    list_filter = ['is_verified', 'verification_date']
    actions = ['verify_drivers', 'unverify_drivers']
    
    def verify_drivers(self, request, queryset):
        updated = queryset.update(is_verified=True, verification_date=timezone.now())
        self.message_user(request, f'{updated} drivers were verified successfully.')
    
    def unverify_drivers(self, request, queryset):
        updated = queryset.update(is_verified=False, verification_date=None)
        self.message_user(request, f'{updated} drivers were unverified.')
    
    verify_drivers.short_description = "Verify selected drivers"
    unverify_drivers.short_description = "Unverify selected drivers"

admin.site.register(DriverProfile, DriverProfileAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PassengerProfile)
# admin.site.register(DriverProfile)