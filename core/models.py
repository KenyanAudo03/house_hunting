from django.db import models

class Amenity(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"

class HostelImage(models.Model):
    hostel = models.ForeignKey('Hostel', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hostel_images/')

    def __str__(self):
        return f"Image for {self.hostel.name}"

class Review(models.Model):
    hostel = models.ForeignKey('Hostel', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.hostel.name} - {self.rating} stars"

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    video = models.FileField(upload_to='hostel_videos/', null=True, blank=True)
    pricing = models.DecimalField(max_digits=10, decimal_places=2)
    available_vacants = models.IntegerField(default=0)
    amenities = models.ManyToManyField(Amenity, blank=True)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0.0