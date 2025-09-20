from django import forms
from accounts.models import RoommateProfile


class RoommateProfileForm(forms.ModelForm):
    class Meta:
        model = RoommateProfile
        fields = ["place_of_stay", "rent", "contact_number", "is_active"]
