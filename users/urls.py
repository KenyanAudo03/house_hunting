from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("profile", views.profile, name="profile"),
    path("favorites", views.favorites, name="favorites"),
    path("roomie-profile", views.roomie_profile, name="roomie_profile"),
]
