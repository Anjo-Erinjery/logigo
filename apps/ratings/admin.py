from django.contrib import admin
from .models import Rating
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['booking', 'customer', 'driver', 'stars', 'created_at']
    list_filter  = ['stars']
