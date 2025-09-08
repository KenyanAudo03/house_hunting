from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Hostel


def home(request):
    hostels = Hostel.objects.all()
    categories = Hostel.CATEGORY_CHOICES
    locations = Hostel.objects.values_list('location', flat=True).distinct()
    
    category = request.GET.get('category', '')
    location = request.GET.get('location', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    query = request.GET.get('q', '')
    
    if category:
        hostels = hostels.filter(category=category)
    if location:
        hostels = hostels.filter(location__icontains=location)
    if min_price:
        hostels = hostels.filter(pricing__gte=min_price)
    if max_price:
        hostels = hostels.filter(pricing__lte=max_price)
    if query:
        hostels = hostels.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(location__icontains=query)
        )
    
    context = {
        'hostels': hostels,
        'categories': categories,
        'locations': locations,
        'selected_category': category,
        'selected_location': location,
        'min_price': min_price,
        'max_price': max_price,
        'query': query,
    }
    return render(request, "core/home.html", context)

def search(request):
    query = request.GET.get("q", "")
    category = request.GET.get("category", "")
    location = request.GET.get("location", "")
    min_price = request.GET.get("min_price", "")
    
    hostels = Hostel.objects.all()
    
    if query:
        hostels = hostels.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(location__icontains=query)
        )
    if category:
        hostels = hostels.filter(category=category)
    if location:
        hostels = hostels.filter(location__icontains=location)
    if min_price:
        hostels = hostels.filter(pricing__gte=min_price)
    
    data = {
        "hostels": [
            {
                "id": h.id,
                "name": h.name,
                "address": h.address,
                "location": h.location,
                "category": h.get_category_display(),
                "pricing": str(h.pricing),
                "available_vacants": h.available_vacants,
                "average_rating": round(h.average_rating, 1) if hasattr(h, 'average_rating') else 0,
                "amenities": [a.name for a in h.amenities.all()],
                "video_url": h.video.url if h.video else None,
            }
            for h in hostels
        ]
    }
    return JsonResponse(data)


def about(request):
    return render(request, "core/about.html")


def contact(request):
    return render(request, "core/contact.html")


def privacy_policy(request):
    return render(request, "core/policy.html")


def terms_of_service(request):
    return render(request, "core/terms.html")


def cookie_policy(request):
    return render(request, "core/cookies.html")


def support(request):
    return render(request, "core/support.html")
