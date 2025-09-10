from django.contrib import admin
from .models import Hostel, HostelImage, Review, Amenity, PropertyListing, HostelInquiry

from django.contrib import admin
from django.utils.text import slugify
from .models import Hostel


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
        "category",
        "pricing",
        "available_vacants",
        "average_rating",
    )
    search_fields = ("name", "address", "location")
    list_filter = ("category", "location")
    filter_horizontal = ("amenities",)
    exclude = ("slug",)


@admin.register(HostelImage)
class HostelImageAdmin(admin.ModelAdmin):
    list_display = ("hostel", "image")
    list_filter = ("hostel",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("hostel", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("hostel__name", "comment")


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(PropertyListing)
class PropertyListingAdmin(admin.ModelAdmin):
    list_display = ("name", "contact", "role", "area", "rent", "hostel", "created_at")
    list_filter = ("role", "created_at")
    search_fields = ("name", "contact", "hostel", "area")
    ordering = ("-created_at",)

    def has_change_permission(self, request, obj=None):
        # Prevent editing while still allowing delete
        return False


@admin.register(HostelInquiry)
class HostelInquiryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "hostel", "created_at")
    list_filter = ("created_at", "hostel")
    search_fields = ("full_name", "email", "hostel__name", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    fieldsets = (
        ("Contact Information", {"fields": ("full_name", "email", "phone")}),
        ("Inquiry Details", {"fields": ("hostel", "message", "created_at")}),
    )

    def has_change_permission(self, request, obj=None):
        # Prevent editing while still allowing delete
        return False
