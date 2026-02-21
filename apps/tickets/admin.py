from django.contrib import admin
from .models import Ticket
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display  = ['ticket_id', 'raised_by', 'subject', 'priority', 'status', 'created_at']
    list_filter   = ['priority', 'status']
    search_fields = ['ticket_id', 'subject']
    list_editable = ['status']
