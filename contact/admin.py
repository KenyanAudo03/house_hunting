from django.contrib import admin
from django.utils.html import format_html
from .models import ContactInquiry, PlatformContact


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email_link", "phone_link", "subject", "created_at")
    list_filter = ("subject", "created_at")
    search_fields = ("first_name", "last_name", "email", "message")
    readonly_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "subject",
        "message",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    full_name.short_description = "Name"

    def email_link(self, obj):
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)

    email_link.short_description = "Email"

    def phone_link(self, obj):
        if obj.phone:
            return format_html('<a href="tel:{}">{}</a>', obj.phone, obj.phone)
        return "-"

    phone_link.short_description = "Phone"

    def has_change_permission(self, request, obj=None):
        # Prevent editing while still allowing deletion
        return False


@admin.register(PlatformContact)
class PlatformContactAdmin(admin.ModelAdmin):
    list_display = ("contact_number", "support_email", "partners_email")
