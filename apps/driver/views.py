from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from apps.bookings.models import Booking, TrackingUpdate
from apps.payments.models import Earnings
from apps.accounts.emails import send_verification_email
from .models import DriverProfile, OCRDocument
from .forms import DriverRegistrationForm
from .ocr import process_document


def driver_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'driver':
            return redirect('login')
        return func(request, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


def register_driver(request):
    form = DriverRegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        # Create DriverProfile
        profile = DriverProfile.objects.create(
            user=user,
            vehicle_type=form.cleaned_data['vehicle_type'],
            vehicle_number=form.cleaned_data['vehicle_number'],
            aadhaar_photo=form.cleaned_data['aadhaar_photo'],
            license_photo=form.cleaned_data['license_photo'],
        )
        # OCR processing
        if profile.aadhaar_photo:
            doc = OCRDocument.objects.create(
                driver=profile, document_type='aadhaar', image=profile.aadhaar_photo
            )
            process_document(doc)
            profile.aadhaar_number = doc.extracted_number
        if profile.license_photo:
            doc = OCRDocument.objects.create(
                driver=profile, document_type='license', image=profile.license_photo
            )
            process_document(doc)
            profile.license_number = doc.extracted_number
        profile.save()
        send_verification_email(user)
        messages.success(request, 'Driver account created! Please verify your email. Documents will be reviewed by admin.')
        return redirect('verify_email_prompt', pk=user.pk)
    return render(request, 'driver/register_driver.html', {'form': form})


@driver_required
def dashboard(request):
    profile  = get_object_or_404(DriverProfile, user=request.user)
    today    = timezone.now().date()
    today_bookings = Booking.objects.filter(driver=request.user, created_at__date=today)
    all_bookings   = Booking.objects.filter(driver=request.user)
    earnings_today = Earnings.objects.filter(driver=request.user, date=today).aggregate(
        total=Sum('amount'))['total'] or 0
    context = {
        'profile':        profile,
        'today_bookings': today_bookings,
        'active_count':   all_bookings.exclude(status__in=['delivered','cancelled']).count(),
        'completed_count':all_bookings.filter(status='delivered').count(),
        'earnings_today': earnings_today,
    }
    return render(request, 'driver/dashboard.html', context)


@driver_required
def new_booking_map(request):
    bookings = Booking.objects.filter(driver=request.user, status__in=['confirmed','picked_up','in_transit'])
    return render(request, 'driver/new_booking.html', {'bookings': bookings})


@driver_required
def earnings(request):
    earns = Earnings.objects.filter(driver=request.user)
    total = earns.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'driver/earnings.html', {'earnings': earns, 'total': total})


@driver_required
def toggle_availability(request):
    profile = get_object_or_404(DriverProfile, user=request.user)
    profile.is_available = not profile.is_available
    profile.save()
    status = 'Online' if profile.is_available else 'Offline'
    messages.success(request, f'You are now {status}.')
    return redirect('driver_dashboard')


@driver_required
def booking_history(request):
    bookings = Booking.objects.filter(driver=request.user)
    return render(request, 'driver/booking_history.html', {'bookings': bookings})


@driver_required
def driver_profile(request):
    from apps.accounts.forms import ProfileUpdateForm
    profile = get_object_or_404(DriverProfile, user=request.user)
    form    = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated.')
    return render(request, 'driver/profile.html', {'form': form, 'profile': profile})


@driver_required
def update_location(request, booking_id):
    """AJAX: Driver sends GPS coords and status update."""
    import json
    if request.method == 'POST':
        data    = json.loads(request.body)
        booking = get_object_or_404(Booking, booking_id=booking_id, driver=request.user)
        TrackingUpdate.objects.create(
            booking=booking,
            lat=data.get('lat', 0),
            lng=data.get('lng', 0),
            status_message=data.get('message', 'En route'),
            updated_by=request.user,
        )
        from django.http import JsonResponse
        return JsonResponse({'success': True})
    from django.http import JsonResponse
    return JsonResponse({'error': 'Method not allowed'}, status=405)
