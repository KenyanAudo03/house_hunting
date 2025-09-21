from django.shortcuts import render
from allauth.account.views import ConfirmEmailView
from django.contrib.auth import login
from django.shortcuts import redirect
import json
import os
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model, login
from django.middleware.csrf import get_token
from google.oauth2 import id_token
from google.auth.transport import requests
from allauth.socialaccount.models import SocialAccount, SocialApp
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import get_adapter
from allauth.account.utils import perform_login
from allauth.socialaccount import app_settings as socialaccount_settings

User = get_user_model()
logger = logging.getLogger(__name__)


class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        if self.object and self.object.email_address:
            user = self.object.email_address.user
            login(
                self.request, user, backend="django.contrib.auth.backends.ModelBackend"
            )
            list(self.request._messages)[:] = []  # Clear existing messages
        return redirect("/")


@csrf_exempt
@require_http_methods(["POST"])
def google_one_tap_login(request):
    """
    Handle Google One Tap authentication using custom social account adapter
    """
    try:
        # Parse request body
        data = json.loads(request.body)
        token = data.get("credential")

        if not token:
            logger.error("No credential provided")
            return JsonResponse({"error": "No credential provided"}, status=400)

        # Get Google client ID from environment or SocialApp
        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        if not client_id:
            try:
                google_app = SocialApp.objects.get(provider=GoogleProvider.id)
                client_id = google_app.client_id
            except SocialApp.DoesNotExist:
                logger.error("Google client ID not configured")
                return JsonResponse(
                    {"error": "Google client ID not configured"}, status=500
                )

        # Verify JWT token with Google
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)
            logger.info(f"Token verified for: {idinfo.get('email')}")
        except ValueError as e:
            logger.error(f"Token verification failed: {e}")
            return JsonResponse({"error": "Invalid token"}, status=400)
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return JsonResponse({"error": "Token verification failed"}, status=400)

        # Validate issuer
        if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            logger.error(f"Invalid issuer: {idinfo['iss']}")
            return JsonResponse({"error": "Invalid token issuer"}, status=400)

        # Extract user data
        email = idinfo.get("email")
        google_id = idinfo.get("sub")
        first_name = idinfo.get("given_name", "")
        last_name = idinfo.get("family_name", "")
        picture_url = idinfo.get("picture", "")

        if not email or not google_id:
            logger.error("Missing email or google_id in token")
            return JsonResponse({"error": "Incomplete user information"}, status=400)

        # Get the social account adapter
        adapter = get_adapter(request)

        # Check for existing social account
        social_account = None
        user = None
        created_user = False

        try:
            # Check if social account already exists
            social_account = SocialAccount.objects.get(
                provider=GoogleProvider.id, uid=google_id
            )
            user = social_account.user
            logger.info(f"Found existing social account for: {email}")

        except SocialAccount.DoesNotExist:
            # Check if user already exists with this email
            try:
                user = User.objects.get(email=email)
                logger.info(
                    f"Found existing user by email, creating social account link: {email}"
                )

                # Create social account for existing user
                social_account = SocialAccount.objects.create(
                    user=user,
                    provider=GoogleProvider.id,
                    uid=google_id,
                    extra_data=idinfo,
                )

            except User.DoesNotExist:
                # Create new user using adapter methods
                logger.info(f"Creating new user: {email}")

                # Generate username using adapter
                username = adapter.generate_username_from_email(email)

                # Create new user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=True,
                )

                # Create social account
                social_account = SocialAccount.objects.create(
                    user=user,
                    provider=GoogleProvider.id,
                    uid=google_id,
                    extra_data=idinfo,
                )

                created_user = True

        if not user:
            logger.error("Failed to create or find user")
            return JsonResponse({"error": "User creation failed"}, status=500)

        # Ensure user is active
        if not user.is_active:
            logger.error(f"User account is inactive: {email}")
            return JsonResponse({"error": "Account is inactive"}, status=400)

        # Handle email verification using adapter approach
        email_address, email_created = EmailAddress.objects.get_or_create(
            user=user, email=email, defaults={"verified": True, "primary": True}
        )

        # Update existing email address if needed
        if not email_address.verified or not email_address.primary:
            email_address.verified = True
            email_address.primary = True
            email_address.save()
            logger.info(f"Updated email verification status for: {email}")

        # Set any other email addresses as non-primary
        EmailAddress.objects.filter(user=user).exclude(id=email_address.id).update(
            primary=False
        )

        # Handle Google avatar using adapter logic
        if picture_url and created_user:
            try:
                from accounts.models import Profile

                profile, profile_created = Profile.objects.get_or_create(user=user)
                profile.google_avatar_url = picture_url
                profile.save(update_fields=["google_avatar_url"])
                logger.info(f"Saved Google avatar for user: {email}")
            except ImportError:
                logger.warning("Profile model doesn't exist")
            except Exception as e:
                logger.warning(f"Failed to save Google avatar: {e}")

        # Perform login using allauth's perform_login
        try:
            perform_login(
                request=request,
                user=user,
                email_verification=socialaccount_settings.EMAIL_VERIFICATION,
                signup=created_user,
                redirect_url=None,
                signal_kwargs={
                    "sociallogin": None,  # We don't have a full SocialLogin object
                    "provider": GoogleProvider.id,
                },
            )
            logger.info(f"User logged in successfully: {email}")

        except Exception as e:
            logger.warning(f"Allauth perform_login failed, using Django login: {e}")
            # Fallback to Django's login
            login(request, user)

        # Ensure session is saved
        if hasattr(request, "session"):
            request.session.save()

        # Get CSRF token for response
        csrf_token = get_token(request)

        return JsonResponse(
            {
                "success": True,
                "redirect_url": "/",
                "message": "Login successful",
                "csrf_token": csrf_token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_new_user": created_user,
                    "is_authenticated": True,
                    "email_verified": email_address.verified,
                    "has_avatar": bool(picture_url) if created_user else False,
                },
            }
        )

    except json.JSONDecodeError:
        logger.error("Invalid JSON in request")
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback

        logger.error(traceback.format_exc())
        return JsonResponse({"error": "Login failed"}, status=500)
