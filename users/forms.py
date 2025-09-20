from django import forms
from accounts.models import RoommateProfile


class RoommateProfileForm(forms.ModelForm):
    class Meta:
        model = RoommateProfile
        fields = ["place_of_stay", "rent", "contact_number", "is_active"]
        widgets = {
            "place_of_stay": forms.TextInput(
                attrs={
                    "class": "roommate-input",
                    "placeholder": "e.g., Waridi Hostel, Sunshine Apartments",
                    "maxlength": 255,
                }
            ),
            "rent": forms.NumberInput(
                attrs={
                    "class": "roommate-input",
                    "placeholder": "e.g., 6000",
                    "min": 0,
                    "step": 1,
                }
            ),
            "contact_number": forms.TextInput(
                attrs={
                    "class": "roommate-input",
                    "placeholder": "e.g., +254700000000 or 0700000000",
                    "pattern": r"^\+?[\d\s\-\(\)]+$",
                    "maxlength": 20,
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "roommate-checkbox",
                }
            ),
        }
        labels = {
            "place_of_stay": "Hostel/Accommodation Location",
            "rent": "Your Share of Rent (KES)",
            "contact_number": "Your Contact Number",
            "is_active": "Make my profile visible to other students",
        }
        help_texts = {
            "place_of_stay": "Enter the name/location of the hostel or accommodation you want to share",
            "rent": "How much you're willing to pay as your share of the total rent",
            "contact_number": "Your phone number for potential roommates to contact you",
            "is_active": "Uncheck to temporarily hide your profile from other students",
        }

    def clean_rent(self):
        rent = self.cleaned_data.get("rent")
        if rent is not None and rent <= 0:
            raise forms.ValidationError("Rent amount must be positive.")
        if rent is not None and rent < 1000:
            raise forms.ValidationError(
                "Rent amount seems too low. Please check the amount."
            )
        if rent is not None and rent > 100000:
            raise forms.ValidationError(
                "Rent amount seems unusually high. Please verify."
            )
        return rent

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get("contact_number")
        if contact_number:
            # Remove spaces and common formatting
            cleaned = (
                contact_number.replace(" ", "")
                .replace("-", "")
                .replace("(", "")
                .replace(")", "")
            )
            if not cleaned.replace("+", "").isdigit():
                raise forms.ValidationError("Please enter a valid phone number.")
            if len(cleaned) < 10:
                raise forms.ValidationError("Phone number is too short.")
            # Check for Kenyan phone number format
            if cleaned.startswith("0") and len(cleaned) == 10:
                # Convert 0700000000 to +254700000000 format for storage
                contact_number = "+254" + cleaned[1:]
            elif cleaned.startswith("+254") and len(cleaned) == 13:
                contact_number = cleaned
            elif cleaned.startswith("254") and len(cleaned) == 12:
                contact_number = "+" + cleaned
            else:
                raise forms.ValidationError("Please enter a valid Kenyan phone number.")
        return contact_number

    def clean_place_of_stay(self):
        place_of_stay = self.cleaned_data.get("place_of_stay")
        if place_of_stay:
            place_of_stay = place_of_stay.strip().title()  # Capitalize properly
            if len(place_of_stay) < 3:
                raise forms.ValidationError(
                    "Location must be at least 3 characters long."
                )
        return place_of_stay
