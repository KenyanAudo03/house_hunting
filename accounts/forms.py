from allauth.account.forms import SignupForm
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
        if "username" in self.fields:
            del self.fields["username"]
        # Update password field placeholders
        self.fields["password1"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirm Password"}
        )

    def generate_username_from_email(self, email):
        """Generate username from email address"""
        # Extract the part before @ symbol
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

    def save(self, request):
        email = self.cleaned_data["email"]
        username = self.generate_username_from_email(email)
        self.cleaned_data["username"] = username
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.username = username
        user.save()
        return user
