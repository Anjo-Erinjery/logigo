from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from .models import CustomUser, EmailVerificationToken
from .forms import LoginForm, CustomerRegistrationForm, OTPVerificationForm
from .emails import send_verification_email


def login_view(request):
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        # Allow login even if email is not verified (only forced after registration)
        login(request, user)
        messages.success(request, f'Welcome back, {user.first_name}!')
        return redirect(user.get_dashboard_url())
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


def register_customer(request):
    form = CustomerRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        send_verification_email(user)
        messages.success(request, 'Account created! Please verify your email.')
        return redirect('verify_email_prompt', pk=user.pk)
    return render(request, 'accounts/register_customer.html', {'form': form})


def verify_email_prompt(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return redirect('login')
    if user.is_email_verified:
        return redirect('login')
    form = OTPVerificationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        otp = form.cleaned_data['otp']
        token = EmailVerificationToken.objects.filter(
            user=user, token=otp, is_used=False
        ).order_by('-created_at').first()
        if token and token.is_valid():
            token.is_used = True
            token.save()
            user.is_email_verified = True
            user.save()
            messages.success(request, 'Email verified! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid or expired OTP. Please try again.')
    return render(request, 'accounts/verify_email.html', {'form': form, 'user_email': user.email, 'pk': pk})


def resend_otp(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return redirect('login')
    if not user.is_email_verified:
        send_verification_email(user)
        messages.success(request, 'A new OTP has been sent to your email.')
    return redirect('verify_email_prompt', pk=pk)
