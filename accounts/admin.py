# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


# Create an inline for Profile
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile Information"
    fields = ("profile_picture", "google_avatar_url", "bio")


# Extend the existing UserAdmin to include Profile inline
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)

# Register the new UserAdmin with Profile inline
admin.site.register(User, CustomUserAdmin)
