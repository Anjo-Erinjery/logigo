from django.urls import path
from . import views
from apps.driver import views as driver_views

urlpatterns = [
    path('login/',               views.login_view,          name='login'),
    path('logout/',              views.logout_view,         name='logout'),
    path('register/customer/',   views.register_customer,   name='register_customer'),
    path('register/driver/',     driver_views.register_driver, name='register_driver'),
    path('verify/<int:pk>/',     views.verify_email_prompt, name='verify_email_prompt'),
    path('resend-otp/<int:pk>/', views.resend_otp,          name='resend_otp'),
]
