from django.urls import path
from . import views
urlpatterns = [
    path('rate/<str:booking_id>/', views.rate_driver, name='rate_driver'),
]
