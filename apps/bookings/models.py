import uuid
from django.db import models
from django.conf import settings


def generate_booking_id():
    return f"DEL-{uuid.uuid4().hex[:8].upper()}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending',     'Pending'),
        ('confirmed',   'Confirmed'),
        ('picked_up',   'Picked Up'),
        ('in_transit',  'In Transit'),
        ('delivered',   'Delivered'),
        ('cancelled',   'Cancelled'),
    ]
    PACKAGE_CHOICES = [
        ('document', 'Document'),
        ('parcel',   'Parcel'),
        ('fragile',  'Fragile'),
        ('bulk',     'Bulk'),
    ]

    booking_id       = models.CharField(max_length=20, unique=True, default=generate_booking_id)
    customer         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         related_name='customer_bookings')
    driver           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='driver_bookings')
    pickup_address   = models.TextField()
    pickup_lat       = models.DecimalField(max_digits=12, decimal_places=7, default=0)
    pickup_lng       = models.DecimalField(max_digits=12, decimal_places=7, default=0)
    item_description = models.TextField(blank=True)
    item_weight      = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    package_type     = models.CharField(max_length=10, choices=PACKAGE_CHOICES, default='parcel')
    is_fragile       = models.BooleanField(default=False)
    status           = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    total_price      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes            = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    actual_delivery  = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.booking_id} — {self.status}"

    def get_drop_count(self):
        return self.drop_locations.count()


class DropLocation(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('delivered', 'Delivered'),
    ]
    booking        = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='drop_locations')
    sequence_order = models.PositiveIntegerField(default=1)
    recipient_name = models.CharField(max_length=100)
    recipient_phone= models.CharField(max_length=15)
    address        = models.TextField()
    lat            = models.DecimalField(max_digits=12, decimal_places=7, default=0)
    lng            = models.DecimalField(max_digits=12, decimal_places=7, default=0)
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    delivered_at   = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['sequence_order']

    def __str__(self):
        return f"Drop {self.sequence_order} — {self.address[:40]}"


class TrackingUpdate(models.Model):
    booking        = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='tracking_updates')
    lat            = models.DecimalField(max_digits=12, decimal_places=7, default=0)
    lng            = models.DecimalField(max_digits=12, decimal_places=7, default=0)
    status_message = models.CharField(max_length=255)
    updated_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.booking.booking_id} — {self.status_message}"
