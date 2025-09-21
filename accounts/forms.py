from allauth.account.forms import SignupForm
from allauth.account.models import EmailAddress
from django import forms
from django.contrib.auth import get_user_model
import re

User = get_user_model()


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label="First Name",
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
    )
    last_name = forms.CharField(
        max_length=30,
        label="Last Name",
        widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove username field if it exists
        if "username" in self.fields:
            del self.fields["username"]

        # Update password field placeholders
        self.fields["password1"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirm Password"}
        )

        # Make sure email field has proper attributes
        self.fields["email"].widget.attrs.update({"placeholder": "Email Address"})

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

    def save(self, request):
        """Save user with custom username generation and names"""
        email = self.cleaned_data["email"]
        username = self.generate_username_from_email(email)

        # Add username to cleaned_data for allauth processing
        self.cleaned_data["username"] = username

        # Save user using parent method
        user = super().save(request)

        # Update user with additional fields
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.username = username
        user.save()

        # Ensure email is marked as verified and primary
        try:
            email_address, created = EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
                defaults={
                    "verified": False,
                    "primary": True,
                },  # Will be verified via email
            )
            if not email_address.primary:
                email_address.primary = True
                email_address.save()
        except Exception:
            # Don't fail form save if email address creation fails
            pass

        return user
