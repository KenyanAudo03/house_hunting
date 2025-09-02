from django.shortcuts import render
from django.http import JsonResponse
from .models import Hostel


def home(request):
    hostels = Hostel.objects.all()
    return render(request, "core/home.html", {"hostels": hostels})


def search(request):
    query = request.GET.get("q", "")
    hostels = Hostel.objects.filter(name__icontains=query)
    data = {
        "hostels": [
            {
                "id": h.id,
                "name": h.name,
                "address": h.address,
                "pricing": str(h.pricing),
                "available_vacants": h.available_vacants,
                "average_rating": round(h.average_rating, 1),
            }
            for h in hostels
        ]
    }
    return JsonResponse(data)


def about(request):
    return render(request, "core/about.html")
