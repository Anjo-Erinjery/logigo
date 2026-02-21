from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


def root_redirect(request):
    if request.user.is_authenticated:
        role = getattr(request.user, 'role', None)
        if role == 'customer':
            return redirect('/customer/dashboard/')
        elif role == 'driver':
            return redirect('/driver/dashboard/')
        elif role == 'admin':
            return redirect('/admin-panel/dashboard/')
    return redirect('/auth/login/')


urlpatterns = [
    path('',               root_redirect,                      name='home'),
    path('auth/',          include('apps.accounts.urls')),
    path('customer/',      include('apps.customer.urls')),
    path('driver/',        include('apps.driver.urls')),
    path('admin-panel/',   include('apps.admin_panel.urls')),
    path('bookings/',      include('apps.bookings.urls')),
    path('payments/',      include('apps.payments.urls')),
    path('tickets/',       include('apps.tickets.urls')),
    path('ratings/',       include('apps.ratings.urls')),
    path('django-admin/',  admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
