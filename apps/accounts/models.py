import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('driver',   'Driver'),
        ('admin',    'Admin'),
    ]
    email           = models.EmailField(unique=True)
    phone_number    = models.CharField(max_length=15, blank=True)
    role            = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    is_email_verified = models.BooleanField(default=False)
    profile_photo   = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    address         = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email}) [{self.role}]"

    def get_dashboard_url(self):
        return {
            'customer': '/customer/dashboard/',
            'driver':   '/driver/dashboard/',
            'admin':    '/admin-panel/dashboard/',
        }.get(self.role, '/auth/login/')


class EmailVerificationToken(models.Model):
    user       = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='otp_tokens')
    token      = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used    = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=15)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    def __str__(self):
        return f"OTP {self.token} for {self.user.email}"
