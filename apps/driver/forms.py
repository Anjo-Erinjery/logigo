from django import forms
from apps.accounts.models import CustomUser
from .models import DriverProfile


class DriverRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )
    vehicle_type = forms.ChoiceField(
        choices=DriverProfile.VEHICLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    vehicle_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vehicle Number'})
    )
    aadhaar_photo = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    license_photo = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )

    class Meta:
        model  = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']
        widgets = {
            'first_name':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email':        forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'address':      forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Address'}),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return p2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def _post_clean(self):
        """Set username = email before Django's unique field validation."""
        email = self.cleaned_data.get('email', '')
        if email:
            self.instance.username = email
        super()._post_clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.role = 'driver'
        if commit:
            user.save()
        return user
