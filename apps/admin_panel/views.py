from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from apps.accounts.models import CustomUser
from apps.bookings.models import Booking, TrackingUpdate
from apps.payments.models import Payment, Earnings
from apps.tickets.models import Ticket
from apps.ratings.models import Rating
from apps.driver.models import DriverProfile


def admin_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return redirect('login')
        return func(request, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@admin_required
def dashboard(request):
    today = timezone.now().date()
    context = {
        'total_users':       CustomUser.objects.filter(role='customer').count(),
        'total_drivers':     CustomUser.objects.filter(role='driver').count(),
        'active_drivers':    DriverProfile.objects.filter(is_available=True).count(),
        'total_bookings':    Booking.objects.count(),
        'active_bookings':   Booking.objects.exclude(status__in=['delivered','cancelled']).count(),
        'today_bookings':    Booking.objects.filter(created_at__date=today).count(),
        'open_tickets':      Ticket.objects.filter(status='open').count(),
        'total_revenue':     Payment.objects.filter(status='success').aggregate(
                                 total=Sum('amount'))['total'] or 0,
        'today_revenue':     Payment.objects.filter(status='success', paid_at__date=today).aggregate(
                                 total=Sum('amount'))['total'] or 0,
        'recent_bookings':   Booking.objects.order_by('-created_at')[:8],
        'pending_drivers':   DriverProfile.objects.filter(is_documents_verified=False).count(),
    }
    return render(request, 'admin_panel/dashboard.html', context)


@admin_required
def manage_users(request):
    q       = request.GET.get('q', '')
    users   = CustomUser.objects.filter(role='customer')
    if q:
        users = users.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q))
    return render(request, 'admin_panel/manage_users.html', {'users': users, 'q': q})


@admin_required
def toggle_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f"User {user.email} {'activated' if user.is_active else 'deactivated'}.")
    return redirect('admin_manage_users')


@admin_required
def manage_drivers(request):
    q       = request.GET.get('q', '')
    drivers = CustomUser.objects.filter(role='driver').select_related('driver_profile')
    if q:
        drivers = drivers.filter(Q(first_name__icontains=q) | Q(email__icontains=q))
    return render(request, 'admin_panel/manage_drivers.html', {'drivers': drivers, 'q': q})


@admin_required
def verify_driver(request, pk):
    profile = get_object_or_404(DriverProfile, pk=pk)
    profile.is_documents_verified = True
    profile.save()
    messages.success(request, f"Driver {profile.user.get_full_name()} documents verified.")
    return redirect('admin_manage_drivers')


@admin_required
def manage_orders(request):
    status  = request.GET.get('status', '')
    orders  = Booking.objects.select_related('customer', 'driver').prefetch_related('drop_locations')
    drivers = CustomUser.objects.filter(role='driver', driver_profile__is_documents_verified=True).select_related('driver_profile')
    if status:
        orders = orders.filter(status=status)
    return render(request, 'admin_panel/manage_orders.html', {
        'orders': orders, 
        'status_filter': status,
        'status_choices': Booking.STATUS_CHOICES,
        'drivers': drivers
    })


@admin_required
def update_order_status(request, booking_id):
    booking    = get_object_or_404(Booking, booking_id=booking_id)
    new_status = request.POST.get('status')
    driver_id  = request.POST.get('driver')

    if new_status in dict(Booking.STATUS_CHOICES):
        booking.status = new_status
    
    if driver_id:
        try:
            driver = CustomUser.objects.get(pk=driver_id, role='driver')
            booking.driver = driver
        except (CustomUser.DoesNotExist, ValueError):
            pass
    elif 'driver' in request.POST and not driver_id:
        booking.driver = None

    booking.save()
    messages.success(request, f'Order {booking_id} updated successfully.')
    return redirect('admin_manage_orders')


@admin_required
def manage_payments(request):
    payments = Payment.objects.select_related('booking__customer').order_by('-paid_at')
    total    = payments.filter(status='success').aggregate(t=Sum('amount'))['t'] or 0
    return render(request, 'admin_panel/manage_payments.html', {'payments': payments, 'total_revenue': total})


@admin_required
def manage_tickets(request):
    status  = request.GET.get('status', '')
    tickets = Ticket.objects.select_related('raised_by')
    if status:
        tickets = tickets.filter(status=status)
    return render(request, 'admin_panel/manage_tickets.html', {'tickets': tickets, 'status_filter': status})


@admin_required
def respond_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    if request.method == 'POST':
        from apps.accounts.emails import send_ticket_response
        ticket.admin_response = request.POST.get('response', '')
        ticket.status         = request.POST.get('status', ticket.status)
        if ticket.status == 'resolved':
            ticket.resolved_at = timezone.now()
        ticket.save()
        send_ticket_response(ticket)
        messages.success(request, f'Ticket {ticket_id} updated and response sent.')
    return redirect('admin_manage_tickets')


@admin_required
def live_tracking(request):
    active_bookings = Booking.objects.exclude(status__in=['delivered','cancelled']).select_related('driver','customer')
    return render(request, 'admin_panel/tracking.html', {'bookings': active_bookings})


@admin_required
def manage_ratings(request):
    ratings = Rating.objects.select_related('customer','driver','booking')
    return render(request, 'admin_panel/manage_ratings.html', {'ratings': ratings})
