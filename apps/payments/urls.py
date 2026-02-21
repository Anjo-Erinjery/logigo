from django.urls import path
from . import views
urlpatterns = [
    path('<str:booking_id>/', views.payment_view, name='payment_view'),
    path('webhook/',          views.razorpay_webhook, name='razorpay_webhook'),
]
