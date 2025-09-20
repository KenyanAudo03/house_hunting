from django.db import models


class ContactInquiry(models.Model):
    SUBJECT_CHOICES = [
        ("housing_search", "Housing Search Help"),
        ("booking_inquiry", "Booking Inquiry"),
        ("property_listing", "Property Listing"),
        ("technical_support", "Technical Support"),
        ("billing", "Billing Question"),
        ("feedback", "Feedback"),
        ("other", "Other"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Inquiry from {self.first_name} {self.last_name} ({self.email})"


class PlatformContact(models.Model):
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_number = models.CharField(max_length=20, blank=True, null=True)
    support_email = models.EmailField(blank=True, null=True)
    partners_email = models.EmailField(blank=True, null=True)
    issues_email = models.EmailField(blank=True, null=True)
    privacy_email = models.EmailField(blank=True, null=True)
    terms_email = models.EmailField(blank=True, null=True)
    cookie_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return "Platform Contact Information"
