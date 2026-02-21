from django.db import models
from django.conf import settings
from apps.bookings.models import Booking


class Payment(models.Model):
    METHOD_CHOICES = [
        ('card',   'Card'),
        ('upi',    'UPI'),
        ('wallet', 'Wallet'),
        ('cod',    'Cash on Delivery'),
    ]
    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('success',  'Success'),
        ('failed',   'Failed'),
        ('refunded', 'Refunded'),
    ]
    booking          = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount           = models.DecimalField(max_digits=10, decimal_places=2)
    method           = models.CharField(max_length=10, choices=METHOD_CHOICES, default='cod')
    status           = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    transaction_id   = models.CharField(max_length=100, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    paid_at          = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-paid_at']

    def __str__(self):
        return f"Payment {self.booking.booking_id} — {self.status} — ₹{self.amount}"


class Earnings(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid',    'Paid'),
    ]
    driver  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='earnings')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='earnings')
    amount  = models.DecimalField(max_digits=10, decimal_places=2)
    date    = models.DateField(auto_now_add=True)
    status  = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Earning ₹{self.amount} for {self.driver.get_full_name()}"
