from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
import re

User = get_user_model()


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def generate_username_from_email(self, email):
        """Generate unique username from email address"""
        base_username = email.split("@")[0]
        base_username = re.sub(r"[^a-zA-Z0-9_]", "", base_username)
        if not base_username:
            base_username = "user"

        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        return username

    def new_user(self, request, sociallogin):
        """Create new user instance"""
        user = User()
        return user

    def populate_user(self, request, sociallogin, data):
        """Populate user information from social provider data"""
        user = super().populate_user(request, sociallogin, data)

        # Generate username from email
        email = data.get("email")
        if email:
            user.username = self.generate_username_from_email(email)
            user.email = email

        # Set names from social data
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        return user

    def save_user(self, request, sociallogin, form=None):
        """Save user and create verified email address"""
        user = super().save_user(request, sociallogin, form)

        # Ensure email is verified and primary
        if user.email:
            email_address, created = EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
                defaults={"verified": True, "primary": True},
            )
            if not email_address.verified or not email_address.primary:
                email_address.verified = True
                email_address.primary = True
                email_address.save()

        # Handle Google avatar URL
        if sociallogin.account.provider == "google":
            extra_data = sociallogin.account.extra_data
            google_avatar_url = extra_data.get("picture")
            if google_avatar_url:
                try:
                    from accounts.models import Profile

                    profile, created = Profile.objects.get_or_create(user=user)
                    profile.google_avatar_url = google_avatar_url
                    profile.save(update_fields=["google_avatar_url"])
                except ImportError:
                    # Profile model doesn't exist
                    pass
                except Exception as e:
                    # Log but don't fail on profile update errors
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.warning(f"Failed to save Google avatar: {e}")

        return user

    def pre_social_login(self, request, sociallogin):
        """Handle existing users trying to connect social account"""
        if sociallogin.is_existing:
            return

        # Check if user already exists with this email
        if sociallogin.user and sociallogin.user.email:
            try:
                existing_user = User.objects.get(email=sociallogin.user.email)
                # Connect the social account to existing user
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                pass
