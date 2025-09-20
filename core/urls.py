from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "submit-property-listing/",
        views.submit_property_listing,
        name="submit_property_listing",
    ),
    path("all-hostels/", views.all_hostel_view, name="all_hostels"),
    path("hostels/<slug:slug>/", views.hostel_detail, name="hostel_detail"),
    path("review/<uuid:token>/", views.leave_review, name="leave_review"),
    path("roommate-list", views.roommate_list, name="roommate_list"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("privacy-policies", views.privacy_policy, name="privacy_policy"),
    path("terms-of-service", views.terms_of_service, name="terms"),
    path("cookie-policies", views.cookie_policy, name="cookies"),
    path("support", views.support, name="support"),
]
