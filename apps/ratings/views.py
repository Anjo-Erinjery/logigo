from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.bookings.models import Booking
from .models import Rating
from .forms import RatingForm


@login_required
def rate_driver(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, customer=request.user, status='delivered')
    if Rating.objects.filter(booking=booking).exists():
        messages.info(request, 'You have already rated this delivery.')
        return redirect('customer_order_history')
    form = RatingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        rating = form.save(commit=False)
        rating.booking  = booking
        rating.customer = request.user
        rating.driver   = booking.driver
        rating.save()
        # Update driver average
        from django.db.models import Avg
        from apps.driver.models import DriverProfile
        avg = Rating.objects.filter(driver=booking.driver).aggregate(avg=Avg('stars'))['avg'] or 0
        dp  = DriverProfile.objects.get(user=booking.driver)
        dp.rating_avg = round(avg, 2)
        dp.save()
        messages.success(request, 'Thank you for your rating!')
        return redirect('customer_order_history')
    return render(request, 'ratings/rate_driver.html', {'form': form, 'booking': booking})
