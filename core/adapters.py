from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
import re

User = get_user_model()


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def generate_username_from_email(self, email):
        """Generate username from email address"""
        base_username = email.split("@")[0]
        # Clean up the username (remove special characters except underscores)
        base_username = re.sub(r"[^a-zA-Z0-9_]", "", base_username)
        # Ensure username is not empty
        if not base_username:
            base_username = "user"

        # Check if username already exists and add number if needed
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        return username

    def populate_user(self, request, sociallogin, data):
        """
        Populates user information from social provider info.
        """
        user = super().populate_user(request, sociallogin, data)
        email = data.get("email")
        if email:
            username = self.generate_username_from_email(email)
            user.username = username
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        return user
