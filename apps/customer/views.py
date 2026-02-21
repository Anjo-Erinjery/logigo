from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.conf import settings
from apps.bookings.models import Booking, DropLocation, TrackingUpdate
from apps.tickets.models import Ticket
from apps.ratings.models import Rating
from apps.payments.models import Payment
from .forms import NewBookingForm, DropLocationFormSet


def customer_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'customer':
            return redirect('login')
        return func(request, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@customer_required
def dashboard(request):
    bookings  = Booking.objects.filter(customer=request.user)
    active    = bookings.exclude(status__in=['delivered', 'cancelled'])
    completed = bookings.filter(status='delivered')
    context = {
        'active_bookings':    active[:5],
        'total_bookings':     bookings.count(),
        'completed_bookings': completed.count(),
        'pending_tickets':    Ticket.objects.filter(raised_by=request.user, status='open').count(),
    }
    return render(request, 'customer/dashboard.html', context)


@customer_required
def new_booking(request):
    form = NewBookingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        booking.customer = request.user
        # Calculate price
        weight   = float(booking.item_weight)
        num_drops = int(request.POST.get('num_drops', 1))
        base_fare = settings.DELIVER_BASE_FARE
        per_km    = settings.DELIVER_PER_KM_RATE
        wt_rate   = settings.DELIVER_WEIGHT_RATE
        md_charge = settings.DELIVER_MULTIDROP_CHARGE
        # Simple estimate (distance 10km default, real calculation via OSRM on frontend)
        dist_km   = float(request.POST.get('distance_km', 10))
        booking.total_price = base_fare + (dist_km * per_km) + (weight * wt_rate) + ((num_drops - 1) * md_charge)
        booking.save()
        # Save drop locations
        for i in range(1, num_drops + 1):
            name  = request.POST.get(f'recipient_name_{i}', '')
            phone = request.POST.get(f'recipient_phone_{i}', '')
            addr  = request.POST.get(f'drop_address_{i}', '')
            lat   = request.POST.get(f'drop_lat_{i}', 0)
            lng   = request.POST.get(f'drop_lng_{i}', 0)
            if name and addr:
                DropLocation.objects.create(
                    booking=booking,
                    sequence_order=i,
                    recipient_name=name,
                    recipient_phone=phone,
                    address=addr,
                    lat=lat if lat else 0,
                    lng=lng if lng else 0,
                )
        messages.success(request, f'Booking {booking.booking_id} placed successfully!')
        return redirect('customer_order_history')
    return render(request, 'customer/new_booking.html', {'form': form})


@customer_required
def order_history(request):
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'customer/order_history.html', {'bookings': bookings})


@customer_required
def tracking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, customer=request.user)
    updates = TrackingUpdate.objects.filter(booking=booking)[:10]
    drops   = booking.drop_locations.all()
    return render(request, 'customer/tracking.html', {'booking': booking, 'updates': updates, 'drops': drops})


@customer_required
def profile(request):
    from apps.accounts.forms import ProfileUpdateForm
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully.')
    return render(request, 'customer/profile.html', {'form': form})


@customer_required
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, customer=request.user)
    payment = Payment.objects.filter(booking=booking).first()
    return render(request, 'customer/payment.html', {'booking': booking, 'payment': payment,
                                                      'razorpay_key': settings.RAZORPAY_KEY_ID})
