from django.contrib import admin
from .models import Payment, Earnings
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'method', 'status', 'paid_at']
    list_filter  = ['status', 'method']
@admin.register(Earnings)
class EarningsAdmin(admin.ModelAdmin):
    list_display = ['driver', 'booking', 'amount', 'date', 'status']
