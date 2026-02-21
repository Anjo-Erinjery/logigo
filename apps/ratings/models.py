from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.bookings.models import Booking


class Rating(models.Model):
    booking    = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='rating')
    customer   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='given_ratings')
    driver     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='received_ratings')
    stars      = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text= models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.stars}★ for {self.driver.get_full_name()} by {self.customer.get_full_name()}"
