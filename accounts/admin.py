from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, RoommateProfile


# Optional: display fields for the list view
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone_number",
        "whatsapp_number",
        "gender",
        "county",
        "town",
        "area_of_stay",
    )
    search_fields = (
        "user__username",
        "phone_number",
        "whatsapp_number",
        "county",
        "town",
    )
    list_filter = ("gender", "county", "town")
    ordering = ("user__username",)
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("user", "profile_picture", "google_avatar_url", "bio")},
        ),
        (
            "Contact",
            {
                "fields": ("phone_number", "whatsapp_number"),
            },
        ),
        (
            "Location & Personal",
            {
                "fields": ("gender", "county", "town", "area_of_stay", "date_of_birth"),
            },
        ),
    )

@admin.register(RoommateProfile)
class RoommateProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "place_of_stay",
        "rent",
        "contact_number",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "place_of_stay", "created_at")
    search_fields = ("user__username", "user__first_name", "user__last_name", "place_of_stay")
    ordering = ("-created_at",)