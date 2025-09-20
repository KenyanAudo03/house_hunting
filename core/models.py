from django.db import models
from django.utils.text import slugify
import uuid
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Amenity(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"


class HostelImage(models.Model):
    hostel = models.ForeignKey(
        "Hostel", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="hostel_images/")

    def __str__(self):
        return f"Image for {self.hostel.name}"


class Review(models.Model):
    hostel = models.ForeignKey(
        "Hostel", on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.hostel.name} - {self.rating} stars"


class ReviewInvitation(models.Model):
    hostel = models.ForeignKey(
        "Hostel", on_delete=models.CASCADE, related_name="review_invitations"
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(max_length=500, blank=True, null=True)
    used = models.BooleanField(default=False)

    def clean(self):
        """Validate that hostel has available vacants"""
        if self._state.adding and self.hostel and self.hostel.available_vacants <= 0:
            raise ValidationError(
                f"Cannot create invitation: {self.hostel.name} has no available slots."
            )

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        # Run validation
        self.full_clean()

        super().save(*args, **kwargs)

        if is_new and self.hostel.available_vacants > 0:
            # Update available vacants
            self.hostel.available_vacants -= 1
            self.hostel.save()

    def set_link(self, request):
        """Set the full absolute URL using the request"""
        if not self.link:
            self.link = self.get_review_link(request)
            self.save(update_fields=["link"])

    def get_review_link(self, request=None):
        """Get the review link - returns stored link or generates new one"""
        if self.link:
            return self.link
        path = reverse("leave_review", args=[str(self.token)])
        if request:
            return request.build_absolute_uri(path)
        return path

    def __str__(self):
        return f"Review invitation for {self.full_name} - {self.hostel.name}"


class HostelInquiry(models.Model):
    hostel = models.ForeignKey(
        "Hostel",
        on_delete=models.CASCADE,
        related_name="inquiries",
        help_text="The hostel this inquiry is about",
    )
    full_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Hostel Inquiry"
        verbose_name_plural = "Hostel Inquiries"

    def __str__(self):
        return f"Inquiry by {self.full_name} for {self.hostel.name}"


class Hostel(models.Model):
    CATEGORY_CHOICES = [
        ("single", "Single Room"),
        ("bedsitter", "Bedsitter"),
        ("one_bedroom", "1 Bedroom"),
        ("two_bedroom", "2 Bedroom"),
    ]

    BILLING_CYCLE_CHOICES = [
        ("month", "Per Month"),
        ("two_months", "Every Two Months"),
        ("semester", "Per Semester"),
    ]

    slug = models.SlugField(unique=True, blank=False, null=False, max_length=255)
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="e.g. Gate A, Bondo town, etc.",
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True
    )
    video = models.FileField(upload_to="hostel_videos/", blank=True, null=True)
    pricing = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False
    )
    billing_cycle = models.CharField(
        max_length=20,
        choices=BILLING_CYCLE_CHOICES,
        default="month",
        blank=True,
        null=True,
        help_text="How often the rent is paid",
    )
    available_vacants = models.IntegerField(default=0)
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Contact phone number for this hostel (e.g. +2547XXXXXXXX)",
    )
    amenities = models.ManyToManyField("Amenity", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0.0

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.name}-{self.location}")
            slug = base_slug
            counter = 1
            while Hostel.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class PropertyListing(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    role = models.CharField(
        max_length=20, choices=[("landlord", "Landlord"), ("tenant", "Tenant")]
    )
    area = models.CharField(max_length=100)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    hostel = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="User who submitted this listing (null for anonymous)",
    )
    reply = models.TextField(
        blank=True, null=True, help_text="Admin reply to this listing"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.role}"
