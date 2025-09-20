from .models import Favorite


def favorites_count(request):
    """
    Context processor to provide favorites count for logged in users
    """
    if request.user.is_authenticated:
        count = Favorite.objects.filter(user=request.user).count()
        return {"favorites_count": count}
    return {"favorites_count": 0}
