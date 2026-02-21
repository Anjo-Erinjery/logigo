# 📦 Deliver Platform — Full Project Documentation

> **Version:** 1.0.0  
> **Stack:** Django 4.2, Python 3.12, SQLite → PostgreSQL ready  
> **Date:** February 2026  
> **Author:** Deliver Dev Team

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Module Breakdown](#3-module-breakdown)
4. [Database Design (ERD)](#4-database-design-erd)
5. [Feature Specifications](#5-feature-specifications)
6. [Authentication & Security](#6-authentication--security)
7. [OCR Integration (Driver Documents)](#7-ocr-integration-driver-documents)
8. [SMTP Email Verification](#8-smtp-email-verification)
9. [Payment Module](#9-payment-module)
10. [Real-Time Tracking](#10-real-time-tracking)
11. [Ticket & Support System](#11-ticket--support-system)
12. [Rating & Review System](#12-rating--review-system)
13. [Django App Structure](#13-django-app-structure)
14. [URL Routing Plan](#14-url-routing-plan)
15. [Tech Stack & Dependencies](#15-tech-stack--dependencies)
16. [Deployment Plan](#16-deployment-plan)
17. [API Endpoints Reference](#17-api-endpoints-reference)
18. [User Flows](#18-user-flows)

---

## 1. Project Overview

**Deliver Platform** is a full-stack courier/delivery management web application built with Django. It mimics the service model of DHL — users can book deliveries from any location to one or multiple destinations (multi-drop support), track packages in real-time, manage payments, and interact with support.

### Core Value Propositions
| Feature | Description |
|---|---|
| Multi-drop bookings | Single pickup, multiple delivery destinations |
| Three user roles | Customer, Driver, Admin — unified login entry point |
| Real-time tracking | Live package location updates |
| OCR document upload | Drivers submit Aadhaar & License, auto-verified via OCR |
| Email SMTP verification | Secure registration for both users and drivers |
| Earnings dashboard | Drivers see live earnings and delivery history |
| Admin control panel | Full oversight of users, drivers, orders, tickets |

---

## 2. System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         Deliver Platform                   │
│                         Django Monolith (MVT)                     │
├───────────────┬──────────────────────┬───────────────────────────┤
│  Customer     │      Driver          │        Admin               │
│  Module       │      Module          │        Module              │
├───────────────┼──────────────────────┼───────────────────────────┤
│ - Book Order  │ - Dashboard          │ - Dashboard (KPIs)         │
│ - Multi-drop  │ - New Booking (map)  │ - Manage Users             │
│ - Tracking    │ - Earnings           │ - Manage Drivers           │
│ - Payments    │ - Availability       │ - Manage Orders            │
│ - History     │ - Booking History    │ - Manage Payments          │
│ - Profile     │ - Tracking           │ - Manage Tickets           │
│ - Rating      │ - Profile            │ - Reports & Analytics      │
│ - Tickets     │ - Verification       │ - Rating Overview          │
└───────────────┴──────────────────────┴───────────────────────────┘
                          │
              ┌───────────▼──────────┐
              │   Django ORM / DB    │
              │   SQLite (dev)       │
              │   PostgreSQL (prod)  │
              └──────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    SMTP Email        OCR Engine       Payment GW
    (Gmail/SendGrid)  (pytesseract)   (Razorpay/Stripe)
```

---

## 3. Module Breakdown

### 3.1 — Customer Module

| Feature | Description |
|---|---|
| Register | Email + password + phone + address. SMTP OTP verification. |
| Login | Single login page, role-based redirect |
| New Booking | Select pickup, add up to 5 drop locations, item details, weight, estimated price |
| Multi-Drop | Map-based route with multiple pins |
| Order History | All past and active orders with status |
| Payment | Pay online (card/UPI/wallet) or COD. Invoice download. |
| Profile | Update personal details, saved addresses |
| Real-time Tracking | Live tracking map for active orders |
| Rating & Review | Rate driver (1–5 stars) after delivery |
| Raise Ticket | Submit support tickets for issues |
| Logout | Session clear |

### 3.2 — Driver Module

| Feature | Description |
|---|---|
| Register | Name, phone, email, vehicle info. Upload Aadhaar + License (OCR). SMTP verification. |
| Login | Same login URL, redirected to driver dashboard |
| Dashboard | Today's orders, earnings, status summary |
| New Booking (Roadmap) | View assigned bookings on an interactive map with route |
| Earnings | Daily/weekly/monthly earnings. Breakdown by delivery. |
| Availability | Toggle online/offline status |
| Booking History | All completed and cancelled trips |
| Real-time Tracking | Driver tracks own route |
| Profile | Update vehicle, bank details, document status |
| Logout | Session clear |

### 3.3 — Admin Module

| Feature | Description |
|---|---|
| Dashboard | Active orders, total users, active drivers, revenue KPIs |
| Manage Users | View, activate/deactivate, search customers |
| Manage Drivers | Approve/reject drivers, verify documents, activate/deactivate |
| Manage Orders | View all bookings, assign drivers, update status |
| Manage Payments | View all transactions, refunds, revenue |
| Manage Tickets | View and respond to support tickets |
| Manage Rating/Review | View all reviews, flag inappropriate ones |
| Real-time Tracking | Track all active deliveries on map |
| Reports | Generate downloadable reports (PDF/CSV) |
| Settings | Email config, pricing config, zones |

---

## 4. Database Design (ERD)

### 4.1 Core Models

#### `CustomUser` (extends AbstractUser)
```
- id (PK)
- email (unique)
- phone_number
- role (ENUM: customer, driver, admin)
- is_email_verified (bool)
- profile_photo
- address
- created_at
- updated_at
```

#### `DriverProfile`
```
- id (PK)
- user (FK → CustomUser)
- vehicle_type (ENUM: bike, auto, van, truck)
- vehicle_number
- aadhaar_photo (ImageField)
- license_photo (ImageField)
- aadhaar_number (OCR extracted)
- license_number (OCR extracted)
- is_documents_verified (bool)
- is_available (bool)
- bank_account_number
- bank_ifsc
- rating_avg (Decimal)
- total_earnings (Decimal)
```

#### `CustomerProfile`
```
- id (PK)
- user (FK → CustomUser)
- saved_addresses (JSONField)
- preferred_payment (ENUM: card, upi, cod)
```

#### `Booking`
```
- id (PK)
- booking_id (unique string, e.g. DEL-2026-001234)
- customer (FK → CustomUser)
- driver (FK → CustomUser, nullable)
- pickup_address (TextField)
- pickup_lat, pickup_lng (Decimal)
- item_description
- item_weight (Decimal)
- package_type (ENUM: document, parcel, fragile, bulk)
- status (ENUM: pending, confirmed, picked_up, in_transit, delivered, cancelled)
- created_at
- estimated_delivery
- actual_delivery
- total_price (Decimal)
- notes
```

#### `DropLocation` (Multi-drop support)
```
- id (PK)
- booking (FK → Booking)
- sequence_order (int)
- recipient_name
- recipient_phone
- address (TextField)
- lat, lng (Decimal)
- status (ENUM: pending, delivered)
- delivered_at
```

#### `TrackingUpdate`
```
- id (PK)
- booking (FK → Booking)
- lat, lng (Decimal)
- status_message
- updated_by (FK → CustomUser)
- timestamp
```

#### `Payment`
```
- id (PK)
- booking (FK → Booking)
- amount (Decimal)
- method (ENUM: card, upi, wallet, cod)
- status (ENUM: pending, success, failed, refunded)
- transaction_id
- gateway_response (JSONField)
- paid_at
```

#### `Earnings`
```
- id (PK)
- driver (FK → CustomUser)
- booking (FK → Booking)
- amount (Decimal)
- date
- status (ENUM: pending, paid)
```

#### `Rating`
```
- id (PK)
- booking (FK → Booking)
- customer (FK → CustomUser)
- driver (FK → CustomUser)
- stars (int, 1–5)
- review_text
- created_at
```

#### `Ticket`
```
- id (PK)
- ticket_id (unique string, e.g. TKT-2026-001)
- raised_by (FK → CustomUser)
- booking (FK → Booking, nullable)
- subject
- description
- priority (ENUM: low, medium, high)
- status (ENUM: open, in_progress, resolved, closed)
- admin_response
- created_at
- resolved_at
```

#### `EmailVerificationToken`
```
- id (PK)
- user (FK → CustomUser)
- token (UUID)
- created_at
- expires_at
- is_used (bool)
```

#### `OCRDocument`
```
- id (PK)
- driver (FK → DriverProfile)
- document_type (ENUM: aadhaar, license)
- image (ImageField)
- extracted_text (TextField)
- extracted_number (CharField)
- is_verified (bool)
- uploaded_at
```

---

## 5. Feature Specifications

### 5.1 New Booking — Multi-Drop Flow

```
Step 1 → Pickup Location (address / GPS)
Step 2 → Add Drop Location(s) [MIN 1, MAX 5]
         - Recipient name + phone
         - Drop address / map pin
         - Add another drop (+)
Step 3 → Package Details
         - Item type, weight, description
         - Fragile? (toggle)
Step 4 → Price Estimation
         - Auto-calculated based on distance + weight + zones
Step 5 → Payment Selection
         - Card / UPI / COD
Step 6 → Confirmation
         - Booking ID displayed
         - Email confirmation sent
Step 7 → Driver Assigned (real-time notification)
```

### 5.2 Pricing Formula

```python
base_fare = 50  # INR
per_km_rate = 12  # INR per km
weight_charge = 5 * item_weight  # INR per kg
multi_drop_charge = (num_drops - 1) * 30  # INR per additional drop

total = base_fare + (distance_km * per_km_rate) + weight_charge + multi_drop_charge
```

---

## 6. Authentication & Security

### Single Login URL (`/auth/login/`)
- User enters email + password
- Django authenticates → checks `role` field
- Redirects:
  - `customer` → `/customer/dashboard/`
  - `driver` → `/driver/dashboard/`
  - `admin` → `/admin-panel/dashboard/`

### Registration Flows
| Role | URL | Extra Steps |
|---|---|---|
| Customer | `/auth/register/customer/` | Email OTP verification |
| Driver | `/auth/register/driver/` | Email OTP + Document upload (OCR) |
| Admin | Created via Django shell / superuser | N/A |

### Security Measures
- CSRF protection on all forms
- Django login_required decorators + custom role decorators
- Passwords hashed with PBKDF2/Argon2
- OTP tokens expire in 15 minutes
- File upload validation (MIME type check)
- Rate limiting on login endpoint

---

## 7. OCR Integration (Driver Documents)

### Library: `pytesseract` + `Pillow`

```python
# Flow:
# 1. Driver uploads Aadhaar / License image
# 2. Image saved to media/driver_docs/
# 3. pytesseract.image_to_string() extracts text
# 4. Regex patterns extract:
#    - Aadhaar: 12-digit number
#    - License: DL format (e.g. MH12 20190012345)
# 5. Extracted data stored in OCRDocument model
# 6. Admin manually approves or system flags auto-verified

AADHAAR_PATTERN = r'\b[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}\b'
LICENSE_PATTERN = r'[A-Z]{2}[0-9]{2}\s?[0-9]{11}'
```

### Document Verification States
```
Uploaded → OCR Processed → Pending Admin Review → Approved / Rejected
```

---

## 8. SMTP Email Verification

### Configuration (settings.py)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your@gmail.com'
EMAIL_HOST_PASSWORD = 'app-password'  # Gmail App Password
```

### Verification Flow
```
1. User registers → OTP (6-digit) generated + stored in EmailVerificationToken
2. Email sent: "Your Deliver verification code is: 123456. Valid for 15 minutes."
3. User enters OTP on verification page
4. On success: is_email_verified = True, user redirected to login
5. On failure/expiry: "Resend OTP" option
```

---

## 9. Payment Module

### Supported Methods
- UPI (via Razorpay)
- Card (Debit/Credit)
- Net Banking
- Cash on Delivery (COD)

### Razorpay Integration Flow
```
1. Order created in Django → Razorpay order created via API
2. Razorpay checkout modal opened on frontend (JS)
3. On payment success: webhook received → Payment model updated
4. Invoice generated (PDF via ReportLab / WeasyPrint)
5. Invoice emailed to customer
```

---

## 10. Real-Time Tracking

### Approach: Django Channels (WebSockets) + Leaflet.js

```
Driver App (mobile/browser) → sends GPS coordinates every 10s
                            → Django Channels consumer receives
                            → TrackingUpdate model saved
                            → Broadcast to customer's tracking page
Customer Tracking Page ← WebSocket connection ← Django Channels
```

### Tracking Map
- **Library:** Leaflet.js (open-source, free)
- **Tile Layer:** OpenStreetMap
- **Route display:** Pickup → Drop 1 → Drop 2 → ... using OSRM API

### Fallback (Simple Mode)
- If WebSockets not available: AJAX polling every 15 seconds

---

## 11. Ticket & Support System

### Ticket Lifecycle
```
Customer/Driver raises ticket
        ↓
Ticket created (status: open)
        ↓
Admin sees in Manage Tickets
        ↓
Admin responds → Email notification sent
        ↓
Status: in_progress → resolved → closed
```

### Ticket Features
- Priority levels: Low / Medium / High / Urgent
- Booking linkage (optional)
- Email notifications at each stage
- Customer can reopen closed tickets

---

## 12. Rating & Review System

### Rules
- Customer can rate only after delivery is confirmed
- One rating per booking
- Driver's `rating_avg` auto-updated after each new rating

### Rating Calculation
```python
def update_driver_rating(driver):
    ratings = Rating.objects.filter(driver=driver)
    avg = ratings.aggregate(Avg('stars'))['stars__avg']
    driver.driverprofile.rating_avg = round(avg, 2)
    driver.driverprofile.save()
```

---

## 13. Django App Structure

```
Deliver/
├── manage.py
├── requirements.txt
├── .env
├── README.md
├── DOCUMENTATION.md
│
├── Deliver/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py              # For Django Channels
│   └── wsgi.py
│
├── apps/
│   ├── accounts/            # Auth, registration, email verification
│   │   ├── models.py        # CustomUser, EmailVerificationToken
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── emails.py        # SMTP helpers
│   │
│   ├── customer/            # Customer module
│   │   ├── models.py        # CustomerProfile
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   │
│   ├── driver/              # Driver module
│   │   ├── models.py        # DriverProfile, OCRDocument
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── ocr.py           # Tesseract OCR helpers
│   │
│   ├── bookings/            # Booking & multi-drop
│   │   ├── models.py        # Booking, DropLocation, TrackingUpdate
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   │
│   ├── payments/            # Payment processing
│   │   ├── models.py        # Payment, Earnings
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── tickets/             # Support tickets
│   │   ├── models.py        # Ticket
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   │
│   ├── ratings/             # Rating & review
│   │   ├── models.py        # Rating
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   │
│   └── admin_panel/         # Custom admin dashboard
│       ├── views.py
│       └── urls.py
│
├── templates/
│   ├── base/
│   │   ├── base.html
│   │   ├── navbar_customer.html
│   │   ├── navbar_driver.html
│   │   └── navbar_admin.html
│   │
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register_customer.html
│   │   ├── register_driver.html
│   │   └── verify_email.html
│   │
│   ├── customer/
│   │   ├── dashboard.html
│   │   ├── new_booking.html
│   │   ├── order_history.html
│   │   ├── tracking.html
│   │   ├── profile.html
│   │   └── payment.html
│   │
│   ├── driver/
│   │   ├── dashboard.html
│   │   ├── new_booking.html
│   │   ├── earnings.html
│   │   ├── availability.html
│   │   ├── booking_history.html
│   │   └── profile.html
│   │
│   ├── admin_panel/
│   │   ├── dashboard.html
│   │   ├── manage_users.html
│   │   ├── manage_drivers.html
│   │   ├── manage_orders.html
│   │   ├── manage_payments.html
│   │   ├── manage_tickets.html
│   │   └── tracking.html
│   │
│   ├── tickets/
│   │   ├── raise_ticket.html
│   │   └── ticket_list.html
│   │
│   └── ratings/
│       └── rate_driver.html
│
├── static/
│   ├── css/
│   │   ├── base.css
│   │   ├── customer.css
│   │   ├── driver.css
│   │   └── admin.css
│   ├── js/
│   │   ├── map.js           # Leaflet integration
│   │   ├── booking.js       # Multi-drop logic
│   │   └── tracking.js      # WebSocket / polling
│   └── images/
│       └── logo.png
│
└── media/                   # User uploads
    ├── profile_photos/
    └── driver_docs/
        ├── aadhaar/
        └── license/
```

---

## 14. URL Routing Plan

```python
# Deliver/urls.py
urlpatterns = [
    path('',                 include('apps.customer.urls')),     # Landing → login redirect
    path('auth/',            include('apps.accounts.urls')),
    path('customer/',        include('apps.customer.urls')),
    path('driver/',          include('apps.driver.urls')),
    path('admin-panel/',     include('apps.admin_panel.urls')),
    path('bookings/',        include('apps.bookings.urls')),
    path('payments/',        include('apps.payments.urls')),
    path('tickets/',         include('apps.tickets.urls')),
    path('ratings/',         include('apps.ratings.urls')),
    path('django-admin/',    admin.site.urls),
]
```

### Key URL Patterns

| URL | View | Role |
|---|---|---|
| `/auth/login/` | LoginView | All |
| `/auth/register/customer/` | CustomerRegisterView | Public |
| `/auth/register/driver/` | DriverRegisterView | Public |
| `/auth/verify-email/<token>/` | VerifyEmailView | All |
| `/customer/dashboard/` | CustomerDashboard | Customer |
| `/customer/new-booking/` | NewBookingView | Customer |
| `/customer/orders/` | OrderHistoryView | Customer |
| `/customer/track/<booking_id>/` | TrackingView | Customer |
| `/customer/payment/<booking_id>/` | PaymentView | Customer |
| `/customer/profile/` | CustomerProfileView | Customer |
| `/customer/rate/<booking_id>/` | RateDriverView | Customer |
| `/customer/tickets/` | TicketListView | Customer |
| `/driver/dashboard/` | DriverDashboard | Driver |
| `/driver/bookings/new/` | DriverNewBookingView | Driver |
| `/driver/earnings/` | DriverEarningsView | Driver |
| `/driver/availability/` | ToggleAvailabilityView | Driver |
| `/driver/history/` | DriverHistoryView | Driver |
| `/driver/profile/` | DriverProfileView | Driver |
| `/admin-panel/dashboard/` | AdminDashboardView | Admin |
| `/admin-panel/users/` | ManageUsersView | Admin |
| `/admin-panel/drivers/` | ManageDriversView | Admin |
| `/admin-panel/orders/` | ManageOrdersView | Admin |
| `/admin-panel/payments/` | ManagePaymentsView | Admin |
| `/admin-panel/tickets/` | ManageTicketsView | Admin |
| `/admin-panel/tracking/` | AdminTrackingView | Admin |
| `/admin-panel/reports/` | ReportsView | Admin |

---

## 15. Tech Stack & Dependencies

```
# requirements.txt

Django==4.2.16
djangorestframework==3.15.2    # For AJAX/API endpoints
channels==4.0.0                # WebSocket real-time tracking
channels-redis==4.1.0          # Channel layer backend
pytesseract==0.3.10            # OCR for Aadhaar/License
Pillow==10.3.0                 # Image processing
python-decouple==3.8           # .env configuration
razorpay==1.4.1                # Payment gateway
reportlab==4.1.0               # PDF invoice generation
django-crispy-forms==2.1       # Beautiful form rendering
crispy-bootstrap5==0.7         # Bootstrap 5 for crispy
django-allauth==0.61.1         # Enhanced auth (optional)
whitenoise==6.6.0              # Static file serving
redis==5.0.1                   # Cache + Channels backend
requests==2.31.0               # HTTP calls (OSRM routing)
geopy==2.4.1                   # Distance calculation
psycopg2-binary==2.9.9         # PostgreSQL (production)
gunicorn==21.2.0               # WSGI server (production)
WeasyPrint==60.2               # HTML→PDF (invoices)
```

### Frontend Libraries (CDN — no npm needed)
- **Bootstrap 5.3** — Layout & components
- **Leaflet.js 1.9** — Interactive maps
- **Chart.js 4.4** — Earnings/analytics charts
- **Font Awesome 6** — Icons
- **SweetAlert2** — Beautiful alerts/notifications

---

## 16. Deployment Plan

### Development
```bash
python manage.py runserver
```

### Production (Ubuntu Server)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure PostgreSQL
createdb Deliver

# 3. Migrations
python manage.py migrate

# 4. Static files
python manage.py collectstatic

# 5. Run with gunicorn + nginx
gunicorn Deliver.wsgi:application --bind 0.0.0.0:8000
```

---

## 17. API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/bookings/estimate/` | Get price estimate |
| POST | `/api/bookings/create/` | Create new booking |
| GET | `/api/bookings/<id>/status/` | Get booking status |
| POST | `/api/driver/location/update/` | Driver sends GPS |
| GET | `/api/tracking/<booking_id>/` | Get live location |
| POST | `/api/payments/initiate/` | Start payment |
| POST | `/api/payments/webhook/` | Razorpay webhook |
| GET | `/api/admin/stats/` | Dashboard KPIs |

---

## 18. User Flows

### Customer Registration Flow
```
Visit Site → Click Register → Select "I'm a Customer"
→ Fill Form (name, email, phone, password, address)
→ Submit → OTP sent to email
→ Enter OTP → Account verified → Login page
→ Enter credentials → Customer Dashboard
```

### Driver Registration Flow
```
Visit Site → Click Register → Select "I'm a Driver"
→ Fill Form (name, email, phone, vehicle type, vehicle no.)
→ Upload Aadhaar Photo → OCR scans → number extracted
→ Upload License Photo → OCR scans → number extracted
→ Submit → OTP sent to email → Verify email
→ Account created (pending document verification)
→ Admin approves documents → Driver can login and work
```

### Booking Flow (Customer)
```
Login → New Booking
→ Set Pickup Location (search / map pin)
→ Add Drop Location 1 (recipient, address)
→ [Optional] Add Drop Location 2, 3, 4, 5
→ Package details → Weight / type / description
→ View estimated price
→ Select payment method → Confirm
→ Booking ID generated → Email sent
→ Nearest available driver auto-assigned
→ Driver accepts → Customer notified
→ Real-time tracking starts
→ Delivery complete → Rate driver option
```

### Admin Operations Flow
```
Admin Login → Admin Dashboard
→ See: Active orders / Revenue / Active drivers / Open tickets
→ Manage Drivers: Review & approve/reject document submissions
→ Manage Orders: View all, filter by status, assign/reassign drivers
→ Manage Tickets: Respond to customer/driver issues
→ Tracking: See all active deliveries on a single map
→ Reports: Export CSV/PDF of orders, payments, earnings
```

---

## Milestones & Timeline

| Phase | Features | Estimated Time |
|---|---|---|
| Phase 1 | Project setup, models, auth, SMTP verification | Week 1 |
| Phase 2 | Customer module (booking, multi-drop, history) | Week 2 |
| Phase 3 | Driver module (dashboard, availability, earnings) | Week 3 |
| Phase 4 | Payment integration (Razorpay + COD) | Week 3–4 |
| Phase 5 | Real-time tracking (Leaflet + Channels) | Week 4–5 |
| Phase 6 | OCR integration, Tickets, Ratings | Week 5–6 |
| Phase 7 | Admin panel, Reports | Week 6–7 |
| Phase 8 | Testing, polishing, deployment | Week 7–8 |

---

*Documentation prepared by Deliver Dev Team — Deliver Platform v1.0*
