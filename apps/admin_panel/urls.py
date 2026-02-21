from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',                          views.dashboard,           name='admin_dashboard'),
    path('users/',                              views.manage_users,        name='admin_manage_users'),
    path('users/toggle/<int:pk>/',              views.toggle_user,         name='admin_toggle_user'),
    path('drivers/',                            views.manage_drivers,      name='admin_manage_drivers'),
    path('drivers/verify/<int:pk>/',            views.verify_driver,       name='admin_verify_driver'),
    path('orders/',                             views.manage_orders,       name='admin_manage_orders'),
    path('orders/status/<str:booking_id>/',     views.update_order_status, name='admin_update_order_status'),
    path('payments/',                           views.manage_payments,     name='admin_manage_payments'),
    path('tickets/',                            views.manage_tickets,      name='admin_manage_tickets'),
    path('tickets/respond/<str:ticket_id>/',    views.respond_ticket,      name='admin_respond_ticket'),
    path('tracking/',                           views.live_tracking,       name='admin_live_tracking'),
    path('ratings/',                            views.manage_ratings,      name='admin_manage_ratings'),
]
