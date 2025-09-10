from django.urls import path
from .views import CustomConfirmEmailView

urlpatterns = [
    path(
        "accounts/confirm-email/<key>/",
        CustomConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
]
