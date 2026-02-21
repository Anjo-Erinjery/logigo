from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    STAR_CHOICES = [(i, f'{i} Star{"s" if i>1 else ""}') for i in range(1,6)]
    stars = forms.ChoiceField(choices=STAR_CHOICES, widget=forms.RadioSelect(attrs={'class': 'star-radio'}))
    class Meta:
        model  = Rating
        fields = ['stars', 'review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your experience...'})
        }
