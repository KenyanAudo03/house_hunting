from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path('toggle-roommate-profile/', views.toggle_roommate_profile, name='toggle_roommate_profile'),
    path("profile", views.profile, name="profile"),
    path("favorites", views.favorites, name="favorites"),
    path(
        "favorites/<int:hostel_id>/toggle/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),  # Add Hostel to favorites
    path("compare-hostels/", views.compare_hostels, name="compare_hostels"),
    path("roomie-profile", views.roomie_profile, name="roomie_profile"),
    path(
        "edit-profile-picture/", views.edit_profile_picture, name="edit_profile_picture"
    ),
    path("edit-name/", views.edit_user_name, name="edit_user_name"),
    path("check-username/", views.check_username, name="check_username"),
    path("check-email/", views.check_email, name="check_email"),
    path("edit-bio/", views.edit_bio, name="edit_bio"),
    path("edit-personal-info/", views.edit_personal_info, name="edit_personal_info"),
    path("edit-contact/", views.edit_contact, name="edit_contact"),
    path(
        "verify-email-change/<uuid:token>/",
        views.verify_email_change,
        name="verify_email_change",
    ),
    path("edit-location/", views.edit_location, name="edit_location"),
    path("edit-password/", views.edit_password, name="edit_password"),
    path("deactivate-account/", views.deactivate_account, name="deactivate_account"),
    path("delete-account/", views.delete_account, name="delete_account"),
]
