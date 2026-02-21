from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',              views.dashboard,     name='customer_dashboard'),
    path('new-booking/',            views.new_booking,   name='customer_new_booking'),
    path('orders/',                 views.order_history, name='customer_order_history'),
    path('track/<str:booking_id>/', views.tracking,      name='customer_tracking'),
    path('payment/<str:booking_id>/', views.payment_view, name='customer_payment'),
    path('profile/',                views.profile,       name='customer_profile'),
]
