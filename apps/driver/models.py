from django.db import models
from django.conf import settings


class DriverProfile(models.Model):
    VEHICLE_CHOICES = [
        ('bike',  'Bike'),
        ('auto',  'Auto'),
        ('van',   'Van'),
        ('truck', 'Truck'),
    ]
    user                  = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                                   related_name='driver_profile')
    vehicle_type          = models.CharField(max_length=10, choices=VEHICLE_CHOICES, default='bike')
    vehicle_number        = models.CharField(max_length=20)
    aadhaar_photo         = models.ImageField(upload_to='driver_docs/aadhaar/', blank=True, null=True)
    license_photo         = models.ImageField(upload_to='driver_docs/license/', blank=True, null=True)
    aadhaar_number        = models.CharField(max_length=20, blank=True)
    license_number        = models.CharField(max_length=30, blank=True)
    is_documents_verified = models.BooleanField(default=False)
    is_available          = models.BooleanField(default=False)
    bank_account_number   = models.CharField(max_length=20, blank=True)
    bank_ifsc             = models.CharField(max_length=15, blank=True)
    rating_avg            = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_earnings        = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ocr_status            = models.CharField(max_length=20, default='pending',
                                              choices=[('pending','Pending'),('processing','Processing'),
                                                       ('done','Done'),('failed','Failed')])

    def __str__(self):
        return f"Driver: {self.user.get_full_name()} | {self.vehicle_type} {self.vehicle_number}"


class OCRDocument(models.Model):
    DOC_TYPE_CHOICES = [
        ('aadhaar', 'Aadhaar'),
        ('license', 'License'),
    ]
    driver           = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name='ocr_docs')
    document_type    = models.CharField(max_length=10, choices=DOC_TYPE_CHOICES)
    image            = models.ImageField(upload_to='driver_docs/ocr/')
    extracted_text   = models.TextField(blank=True)
    extracted_number = models.CharField(max_length=50, blank=True)
    is_verified      = models.BooleanField(default=False)
    uploaded_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.driver.user.get_full_name()} — {self.document_type}"


class CustomerProfile(models.Model):
    PAYMENT_CHOICES = [
        ('card', 'Card'),
        ('upi',  'UPI'),
        ('cod',  'Cash on Delivery'),
    ]
    user              = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                              related_name='customer_profile')
    saved_addresses   = models.JSONField(default=list, blank=True)
    preferred_payment = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cod')

    def __str__(self):
        return f"Customer: {self.user.get_full_name()}"
