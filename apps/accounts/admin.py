from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailVerificationToken


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display  = ['email', 'first_name', 'last_name', 'role', 'is_email_verified', 'is_active']
    list_filter   = ['role', 'is_email_verified', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering      = ['-date_joined']
    fieldsets     = UserAdmin.fieldsets + (
        ('Deliver Info', {'fields': ('role', 'phone_number', 'address', 'is_email_verified', 'profile_photo')}),
    )


@admin.register(EmailVerificationToken)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'is_used', 'expires_at']
    list_filter  = ['is_used']
