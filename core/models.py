from django.db import models
from django.utils.text import slugify


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
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    location = models.CharField(
        max_length=100, help_text="e.g. Gate A, Bondo town, etc."
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    video = models.FileField(upload_to="hostel_videos/", null=True, blank=True)
    pricing = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(
        max_length=20,
        choices=BILLING_CYCLE_CHOICES,
        default="month",
        help_text="How often the rent is paid",
    )
    available_vacants = models.IntegerField(default=0)
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.role}"
