# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
    google_avatar_url = models.URLField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True
    )
    county = models.CharField(max_length=50, default="Siaya")
    town = models.CharField(max_length=50, default="Bondo")
    area_of_stay = models.CharField(
        max_length=100, blank=True, null=True
    )  # e.g., Gate A
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "Other User Detail"
        verbose_name_plural = "Other Users Details"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create profile for new users, but don't interfere with existing profiles
    """
    if created:
        # Only create profile for new users
        Profile.objects.create(user=instance)
    else:
        # For existing users, only create profile if it doesn't exist
        try:
            instance.profile
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)
