from django.contrib import admin
from .models import Booking, DropLocation, TrackingUpdate

class DropLocationInline(admin.TabularInline):
    model = DropLocation
    extra = 0

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ['booking_id', 'customer', 'driver', 'status', 'total_price', 'created_at']
    list_filter   = ['status', 'package_type']
    search_fields = ['booking_id', 'customer__email']
    list_editable = ['status', 'driver']
    inlines       = [DropLocationInline]

@admin.register(TrackingUpdate)
class TrackingAdmin(admin.ModelAdmin):
    list_display = ['booking', 'status_message', 'timestamp']
