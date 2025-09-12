from django.urls import path
from . import views

urlpatterns = [
    path("submit-contact-inquiry/", views.submit_contact_inquiry, name="submit_contact_inquiry"), 
]
