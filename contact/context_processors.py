from .models import PlatformContact

def platform_contact(request):
    contact = PlatformContact.objects.first()
    return {
        "platform_contact": contact,
    }