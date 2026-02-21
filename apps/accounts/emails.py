import random
import string
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from .models import EmailVerificationToken


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


def send_verification_email(user):
    # Invalidate existing unused tokens
    EmailVerificationToken.objects.filter(user=user, is_used=False).update(is_used=True)

    otp = generate_otp()
    token = EmailVerificationToken.objects.create(
        user=user,
        token=otp,
        expires_at=timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES),
    )

    subject = 'Your Deliver Verification Code'
    message = (
        f"Hello {user.first_name},\n\n"
        f"Your Deliver verification code is: {otp}\n\n"
        f"This code is valid for {settings.OTP_EXPIRY_MINUTES} minutes.\n\n"
        f"If you did not request this, please ignore this email.\n\n"
        f"— The Deliver Team"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    return token


def send_booking_confirmation(user, booking):
    subject = f'Booking Confirmed — {booking.booking_id}'
    message = (
        f"Hello {user.first_name},\n\n"
        f"Your delivery has been booked successfully!\n\n"
        f"Booking ID : {booking.booking_id}\n"
        f"Pickup     : {booking.pickup_address}\n"
        f"Total Price: ₹{booking.total_price}\n\n"
        f"You can track your delivery at: http://127.0.0.1:8000/customer/track/{booking.booking_id}/\n\n"
        f"— The Deliver Team"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def send_ticket_response(ticket):
    subject = f'Update on Your Ticket — {ticket.ticket_id}'
    message = (
        f"Hello {ticket.raised_by.first_name},\n\n"
        f"Your support ticket has been updated.\n\n"
        f"Ticket ID : {ticket.ticket_id}\n"
        f"Status    : {ticket.get_status_display()}\n"
        f"Response  : {ticket.admin_response or 'Under review'}\n\n"
        f"— The Deliver Support Team"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [ticket.raised_by.email])
