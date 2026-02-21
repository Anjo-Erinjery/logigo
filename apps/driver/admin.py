from django.contrib import admin
from .models import DriverProfile, OCRDocument, CustomerProfile

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle_type', 'vehicle_number', 'is_documents_verified', 'is_available', 'rating_avg']
    list_filter  = ['is_documents_verified', 'is_available', 'vehicle_type']
    list_editable= ['is_documents_verified', 'is_available']

@admin.register(OCRDocument)
class OCRDocumentAdmin(admin.ModelAdmin):
    list_display = ['driver', 'document_type', 'extracted_number', 'is_verified', 'uploaded_at']
    list_editable= ['is_verified']

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'preferred_payment']
