from django import forms
from apps.bookings.models import Booking


class NewBookingForm(forms.ModelForm):
    class Meta:
        model  = Booking
        fields = ['pickup_address', 'pickup_lat', 'pickup_lng',
                  'item_description', 'item_weight', 'package_type', 'is_fragile', 'notes']
        widgets = {
            'pickup_address':   forms.TextInput(attrs={'class': 'form-control', 'id': 'pickup_address',
                                                        'placeholder': 'Pickup address'}),
            'pickup_lat':       forms.HiddenInput(),
            'pickup_lng':       forms.HiddenInput(),
            'item_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2,
                                                       'placeholder': 'Describe your item(s)'}),
            'item_weight':      forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1',
                                                          'placeholder': 'Weight in kg'}),
            'package_type':     forms.Select(attrs={'class': 'form-select'}),
            'is_fragile':       forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes':            forms.Textarea(attrs={'class': 'form-control', 'rows': 2,
                                                       'placeholder': 'Special instructions (optional)'}),
        }

DropLocationFormSet = None  # handled via raw POST in views
