from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import json
import re
from allauth.account.models import EmailAddress
from accounts.models import EmailChangeRequest
from .sanitizer import (
    clean_text,
    clean_username,
    clean_phone,
    clean_bio,
    clean_email,
)


@login_required
def dashboard(request):
    return render(request, "users/dashboard.html")


@login_required
def profile(request):
    return render(
        request,
        "users/profile.html",
        {"has_usable_password": request.user.has_usable_password()},
    )


# Edit profile picture
@login_required
def edit_profile_picture(request):
    if request.method == "POST":
        profile = request.user.profile
        if "profile_picture" in request.FILES:
            profile.picture = request.FILES["profile_picture"]
            profile.save()
            messages.success(request, "Profile picture updated successfully!")
        return redirect("users:profile")
    return render(request, "users/profile.html")


# Edit username
@login_required
def edit_user_name(request):
    if request.method == "POST":
        first_name = clean_text(request.POST.get("first_name"))
        last_name = clean_text(request.POST.get("last_name"))
        username = clean_username(request.POST.get("username"))

        if username and username != request.user.username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect("users:profile")

        if username is None:
            messages.error(request, "Invalid username format.")
            return redirect("users:profile")

        if first_name is None or last_name is None:
            messages.error(
                request, "Names can only contain letters and simple characters."
            )
            return redirect("users:profile")

        if first_name:
            request.user.first_name = first_name
        if last_name:
            request.user.last_name = last_name
        if username:
            request.user.username = username

        request.user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("users:profile")
    return render(request, "users/profile.html")


@csrf_exempt
def check_username(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = clean_username(data.get("username"))

        if username and username != request.user.username:
            exists = User.objects.filter(username=username).exists()
            return JsonResponse({"exists": exists})
        return JsonResponse({"exists": False})
    return JsonResponse({"exists": False})


# Edit bio
@login_required
def edit_bio(request):
    if request.method == "POST":
        new_bio = clean_bio(request.POST.get("bio"))
        if new_bio is not None:
            request.user.profile.bio = new_bio
            request.user.profile.save()
            messages.success(request, "Bio updated successfully!")
        else:
            messages.error(request, "Invalid bio content.")
        return redirect("users:profile")
    return render(request, "users/profile.html")


# Edit personal info
@login_required
def edit_personal_info(request):
    if request.method == "POST":
        profile = request.user.profile
        first_name = clean_text(request.POST.get("first_name"))
        last_name = clean_text(request.POST.get("last_name"))
        dob = request.POST.get("date_of_birth")

        if first_name is None or last_name is None:
            messages.error(request, "Invalid characters in name fields.")
            return redirect("users:profile")

        if first_name:
            profile.first_name = first_name
        if last_name:
            profile.last_name = last_name
        if dob:
            profile.date_of_birth = dob

        profile.save()
        messages.success(request, "Personal information updated successfully!")
        return redirect("users:profile")
    return render(request, "users/profile.html")


# Edit contact info
@login_required
def edit_contact(request):
    if request.method == "POST":
        user = request.user
        profile = user.profile
        email = request.POST.get("email", "").strip()
        phone = clean_phone(request.POST.get("phone_number"))
        whatsapp_number = clean_phone(request.POST.get("whatsapp_number"))

        if phone is None and request.POST.get("phone_number"):
            messages.error(request, "Invalid phone number format.")
            return redirect("users:profile")
        if whatsapp_number is None and request.POST.get("whatsapp_number"):
            messages.error(request, "Invalid WhatsApp number format.")
            return redirect("users:profile")

        if email and not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            messages.error(request, "Invalid email address.")
            return redirect("users:profile")

        if email and User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, "This email is already registered.")
            return redirect("users:profile")

        email_changed = False
        if email and email != user.email:
            existing_request = EmailChangeRequest.objects.filter(
                user=user, new_email=email, is_verified=False
            ).first()

            if existing_request and not existing_request.is_expired():
                messages.info(
                    request,
                    f"A verification email was already sent to {email}.",
                )
                return redirect("users:profile")

            EmailChangeRequest.objects.filter(user=user, is_verified=False).delete()
            email_request = EmailChangeRequest.objects.create(
                user=user, new_email=email
            )
            send_email_verification(request, email_request)
            email_changed = True

        if phone:
            profile.phone_number = phone
        if whatsapp_number:
            profile.whatsapp_number = whatsapp_number
        profile.save()

        if email_changed:
            messages.info(
                request,
                f"A verification email has been sent to {email}.",
            )
        else:
            messages.success(request, "Contact information updated successfully!")
        return redirect("users:profile")
    return render(request, "users/profile.html")


def send_email_verification(request, email_request):
    verification_url = request.build_absolute_uri(
        reverse("users:verify_email_change", kwargs={"token": email_request.token})
    )
    subject = "Verify Your New Email Address"
    html_message = render_to_string(
        "emails/verify_email_change.html",
        {
            "user": email_request.user,
            "new_email": email_request.new_email,
            "verification_url": verification_url,
            "expires_at": email_request.expires_at,
        },
    )
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [email_request.new_email],
        html_message=html_message,
    )


def verify_email_change(request, token):
    email_request = get_object_or_404(EmailChangeRequest, token=token)
    if email_request.is_expired():
        messages.error(request, "This verification link has expired.")
        return redirect("users:profile")

    if email_request.is_verified:
        messages.info(request, "This email has already been verified.")
        return redirect("users:profile")

    if (
        User.objects.filter(email=email_request.new_email)
        .exclude(pk=email_request.user.pk)
        .exists()
    ):
        messages.error(request, "This email address is no longer available.")
        email_request.delete()
        return redirect("users:profile")

    user = email_request.user
    old_email = user.email
    user.email = email_request.new_email
    user.save()

    EmailAddress.objects.filter(user=user, primary=True).update(primary=False)
    EmailAddress.objects.filter(user=user, email=old_email).delete()
    email_address, created = EmailAddress.objects.get_or_create(
        user=user,
        email=email_request.new_email,
        defaults={"verified": True, "primary": True},
    )
    if not created:
        email_address.verified = True
        email_address.primary = True
        email_address.save()
    EmailAddress.objects.filter(user=user).exclude(pk=email_address.pk).delete()

    email_request.is_verified = True
    email_request.save()
    EmailChangeRequest.objects.filter(user=user, is_verified=False).delete()

    messages.success(
        request, f"Your email has been updated to {email_request.new_email}"
    )
    return redirect("users:profile")


@csrf_exempt
def check_email(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"exists": False, "error": "Invalid JSON"}, status=400)
        email = clean_email(data.get("email"))
        if email and email != request.user.email:
            exists = User.objects.filter(email=email).exists()
            return JsonResponse({"exists": exists})
        return JsonResponse({"exists": False})
    return JsonResponse({"exists": False}, status=405)


# Edit location
@login_required
def edit_location(request):
    if request.method == "POST":
        profile = request.user.profile
        county = clean_text(request.POST.get("county"))
        town = clean_text(request.POST.get("town"))
        area_of_stay = clean_text(request.POST.get("area_of_stay"))

        if county is None or town is None or area_of_stay is None:
            messages.error(request, "Invalid characters in location.")
            return redirect("users:profile")

        profile.county = county
        profile.town = town
        profile.area_of_stay = area_of_stay
        profile.save()

        messages.success(request, "Location updated successfully!")
        return redirect("users:profile")

    return render(request, "users/profile.html")


# Edit password
@login_required
def edit_password(request):
    if request.method == "POST":
        user = request.user
        has_password = user.has_usable_password()

        if has_password:
            current_password = request.POST.get("current_password")
            if not user.check_password(current_password):
                messages.error(request, "Current password is incorrect.")
                return redirect("users:profile")

        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("users:profile")

        # Custom complexity check
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[\d\W]).{8,}$"
        if not re.match(pattern, new_password):
            messages.error(
                request,
                "Password must be at least 8 characters long, contain uppercase, "
                "lowercase, and at least a number or special character.",
            )
            return redirect("users:profile")

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            messages.error(request, " ".join(e.messages))
            return redirect("users:profile")

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(
            request,
            (
                "Password updated successfully!"
                if has_password
                else "Password set successfully!"
            ),
        )
        return redirect("users:profile")

    return render(request, "users/profile.html")


# Deactivate account
@login_required
def deactivate_account(request):
    if request.method == "POST":
        request.user.is_active = False
        request.user.save()
        logout(request)
        messages.success(request, "Your account has been deactivated.")
        return redirect("/accounts/login/")
    return render(request, "users/profile.html")


# Delete Account
@login_required
def delete_account(request):
    if request.method == "POST":
        password = request.POST.get("password", "").strip()
        user = request.user

        if not user.check_password(password):
            messages.error(request, "Password is incorrect. Account not deleted.")
            return redirect("users:profile")

        user.delete()
        messages.success(request, "Your account has been permanently deleted.")
        return redirect("/accounts/signup/")

    return render(request, "users/profile.html")


@login_required
def favorites(request):
    return render(request, "users/favorites.html")


@login_required
def roomie_profile(request):
    return render(request, "users/roomie_profile.html")
