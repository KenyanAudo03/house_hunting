from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("privacy_policies", views.privacy_policy, name="privacy_policy"),
    path("terms_of_service", views.terms_of_service, name="terms"),
    path("cookie_policies", views.cookie_policy, name="cookies"),
    path("support", views.support, name="support"),
]
