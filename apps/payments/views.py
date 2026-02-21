from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from apps.bookings.models import Booking
from .models import Payment
import json


@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    payment, _ = Payment.objects.get_or_create(booking=booking, defaults={'amount': booking.total_price})
    return render(request, 'customer/payment.html', {'booking': booking, 'payment': payment})


@csrf_exempt
def razorpay_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event = data.get('event')
            if event == 'payment.captured':
                payload    = data['payload']['payment']['entity']
                txn_id     = payload.get('id')
                order_id   = payload.get('order_id', '')
                # Find booking via notes/order_id
                payments = Payment.objects.filter(transaction_id=order_id)
                for p in payments:
                    p.status       = 'success'
                    p.transaction_id = txn_id
                    p.gateway_response = payload
                    p.paid_at      = timezone.now()
                    p.save()
                    p.booking.status = 'confirmed'
                    p.booking.save()
        except Exception:
            pass
    return JsonResponse({'status': 'ok'})
