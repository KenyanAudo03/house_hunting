from .models import PlatformContact

def platform_contact(request):
    contact = PlatformContact.objects.first()  # you probably only keep one record
    return {
        "platform_contact": contact,
    }