from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model  = Ticket
        fields = ['subject', 'description', 'priority', 'booking']
        widgets = {
            'subject':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief subject'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your issue'}),
            'priority':    forms.Select(attrs={'class': 'form-select'}),
            'booking':     forms.Select(attrs={'class': 'form-select'}),
        }
