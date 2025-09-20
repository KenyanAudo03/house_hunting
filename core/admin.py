from django.contrib import admin
from .models import (
    Hostel,
    HostelImage,
    Review,
    Amenity,
    PropertyListing,
    HostelInquiry,
    ReviewInvitation,
)
from django.core.mail import send_mail
from django.utils.html import format_html
from django.contrib import admin
from .models import Hostel
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from datetime import datetime


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
    list_display = (
        "name",
        "contact_link",
        "role",
        "area",
        "rent",
        "hostel",
        "user_display",
        "has_reply",
        "created_at",
    )
    list_filter = ("role", "created_at", "user__isnull")
    search_fields = ("name", "contact", "hostel", "area", "user__username")
    ordering = ("-created_at",)
    readonly_fields = (
        "name",
        "contact",
        "role",
        "area",
        "rent",
        "hostel",
        "user",
        "created_at",
    )
    fields = (
        "name",
        "contact",
        "role",
        "area",
        "rent",
        "hostel",
        "user",
        "created_at",
        "reply",
    )

    def contact_link(self, obj):
        if obj.contact and "@" in obj.contact:
            return format_html('<a href="mailto:{}">{}</a>', obj.contact, obj.contact)
        elif obj.contact:
            return format_html('<a href="tel:{}">{}</a>', obj.contact, obj.contact)
        return "-"

    contact_link.short_description = "Contact"

    def user_display(self, obj):
        return obj.user.username if obj.user else "Anonymous"

    user_display.short_description = "User"

    def has_reply(self, obj):
        return "Yes" if obj.reply else "No"

    has_reply.short_description = "Replied"
    has_reply.boolean = True

    def has_change_permission(self, request, obj=None):
        return True  # Allow editing for reply field

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(HostelInquiry)
class HostelInquiryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email_link", "phone_link", "hostel", "created_at")
    list_filter = ("created_at", "hostel")
    search_fields = ("full_name", "email", "hostel__name", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    fieldsets = (
        ("Contact Information", {"fields": ("full_name", "email", "phone")}),
        ("Inquiry Details", {"fields": ("hostel", "message", "created_at")}),
    )

    def email_link(self, obj):
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)

    email_link.short_description = "Email"

    def phone_link(self, obj):
        if obj.phone:
            return format_html('<a href="tel:{}">{}</a>', obj.phone, obj.phone)
        return "-"

    phone_link.short_description = "Phone"

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ReviewInvitation)
class ReviewInvitationAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone",
        "hostel",
        "created_at",
        "used",
        "review_link_display",
    )
    readonly_fields = ("used", "link")

    class Media:
        js = ("admin/js/review_link_copy.js",)

    def review_link_display(self, obj):
        """Display the link with copy button"""
        link = obj.link or obj.get_review_link()
        return format_html(
            '<div style="display: flex; align-items: center;">'
            '<input type="text" value="{}" id="link-{}" readonly style="width:350px; margin-right: 5px;"> '
            '<button type="button" onclick="copyToClipboard(\'link-{}\')" style="padding: 2px 8px;">Copy</button>'
            "</div>",
            link,
            obj.pk,
            obj.pk,
        )

    review_link_display.short_description = "Review Link"

    def save_model(self, request, obj, form, change):
        # Block creation if hostel has no available slots
        if not change and obj.hostel.available_vacants <= 0:
            messages.error(
                request,
                f"Cannot create invitation: {obj.hostel.name} has no available slots.",
            )
            return

        super().save_model(request, obj, form, change)

        if not change:  # New invitation
            obj.set_link(request)

            if obj.email:
                self.send_review_invitation_email(obj, request)

    def send_review_invitation_email(self, invitation, request):
        """Send an HTML review invitation email"""
        try:
            context = {
                "invitation": invitation,
                "hostel": invitation.hostel,
                "year": datetime.now().year,
            }
            html_content = render_to_string("emails/review_invitation.html", context)

            subject = f"Share Your Experience at {invitation.hostel.name}"
            from_email = settings.EMAIL_HOST_USER
            recipient = [invitation.email]

            email = EmailMultiAlternatives(
                subject=subject,
                body="Please view this email in HTML format.",
                from_email=from_email,
                to=recipient,
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            messages.success(
                request, f"Review invitation sent successfully to {invitation.email}"
            )

        except Exception as e:
            messages.error(
                request,
                f"Failed to send review invitation email: {e}",
            )
