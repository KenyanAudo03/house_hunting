from .models import PropertyListing
import os

def google_client_id(request):
    return {
        "google_client_id": os.environ.get("GOOGLE_CLIENT_ID", "")
    }


def user_listings_count(request):
    """
    Context processor to provide user listings count for logged in users
    """
    if request.user.is_authenticated:
        count = PropertyListing.objects.filter(user=request.user).count()
        return {"user_listings_count": count}
    return {"user_listings_count": 0}
