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
