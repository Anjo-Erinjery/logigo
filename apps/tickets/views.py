from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm
from apps.accounts.emails import send_ticket_response


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(raised_by=request.user)
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})


@login_required
def raise_ticket(request):
    form = TicketForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        ticket = form.save(commit=False)
        ticket.raised_by = request.user
        ticket.save()
        messages.success(request, f'Ticket {ticket.ticket_id} raised successfully!')
        return redirect('ticket_list')
    return render(request, 'tickets/raise_ticket.html', {'form': form})
