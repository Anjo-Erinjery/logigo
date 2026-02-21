from django.urls import path
from . import views

urlpatterns = [
    path('register/',               views.register_driver,    name='register_driver'),
    path('dashboard/',              views.dashboard,           name='driver_dashboard'),
    path('bookings/map/',           views.new_booking_map,     name='driver_new_booking'),
    path('earnings/',               views.earnings,            name='driver_earnings'),
    path('availability/',           views.toggle_availability, name='driver_availability'),
    path('history/',                views.booking_history,     name='driver_booking_history'),
    path('profile/',                views.driver_profile,      name='driver_profile'),
    path('update-location/<str:booking_id>/', views.update_location, name='driver_update_location'),
    path('mark-picked-up/<str:booking_id>/', views.mark_as_picked_up, name='mark_as_picked_up'),
    path('mark-drop-delivered/<int:drop_id>/', views.mark_drop_delivered, name='mark_drop_delivered'),
]
