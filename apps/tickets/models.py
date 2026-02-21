import uuid
from django.db import models
from django.conf import settings
from apps.bookings.models import Booking


def generate_ticket_id():
    return f"TKT-{uuid.uuid4().hex[:6].upper()}"


class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ('low',    'Low'),
        ('medium', 'Medium'),
        ('high',   'High'),
        ('urgent', 'Urgent'),
    ]
    STATUS_CHOICES = [
        ('open',        'Open'),
        ('in_progress', 'In Progress'),
        ('resolved',    'Resolved'),
        ('closed',      'Closed'),
    ]
    ticket_id      = models.CharField(max_length=15, unique=True, default=generate_ticket_id)
    raised_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                        related_name='tickets')
    booking        = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='tickets')
    subject        = models.CharField(max_length=200)
    description    = models.TextField()
    priority       = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status         = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    admin_response = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    resolved_at    = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.ticket_id} — {self.subject}"
