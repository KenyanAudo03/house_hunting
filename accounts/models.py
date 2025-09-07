# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
    google_avatar_url = models.URLField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


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
