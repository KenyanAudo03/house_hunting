from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from accounts.views import CustomConfirmEmailView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/confirm-email/<key>/",
        CustomConfirmEmailView.as_view(),
        name="account_confirm_email",
    ), # Custom email confirmation view to auto-login after confirmation
    path("accounts/", include("allauth.urls")),
    path("", include("core.urls")),
    path("contact/", include("contact.urls")),
    path("users/", include("users.urls")), # Keep user account urls separately
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
