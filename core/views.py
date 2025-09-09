from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Hostel, PropertyListing
import re
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.http import require_http_methods
import json


def home(request):
    now = timezone.now()
    three_days_ago = now - timedelta(days=3)

    # Hostels created within 3 days and still available
    latest_hostels_qs = Hostel.objects.filter(
        created_at__gte=three_days_ago, available_vacants__gt=0
    )

    # Hostels older than 3 days and still available
    more_hostels_qs = Hostel.objects.filter(
        created_at__lt=three_days_ago, available_vacants__gt=0
    )

    categories = Hostel.CATEGORY_CHOICES
    locations = Hostel.objects.values_list("location", flat=True).distinct()
    query = request.GET.get("q", "")

    if query:
        search_filter = Q()
        query_words = query.split()
        price_numbers = re.findall(r"\d+", query)

        for word in query_words:
            word_filter = (
                Q(name__icontains=word)
                | Q(address__icontains=word)
                | Q(location__icontains=word)
                | Q(description__icontains=word)
            )

            for choice_key, choice_display in categories:
                if word.lower() in choice_display.lower():
                    word_filter |= Q(category=choice_key)

            search_filter &= word_filter

        if price_numbers:
            price_filter = Q()
            for price_str in price_numbers:
                price_value = int(price_str)
                price_filter |= Q(
                    pricing__gte=price_value - 500, pricing__lte=price_value + 500
                )
            search_filter &= price_filter

        latest_hostels_qs = latest_hostels_qs.filter(search_filter)
        more_hostels_qs = more_hostels_qs.filter(search_filter)

    latest_hostels_qs = latest_hostels_qs.order_by("-created_at")
    more_hostels_qs = more_hostels_qs.order_by("-created_at")

    latest_hostels = latest_hostels_qs[:15]
    more_hostels = more_hostels_qs[:15]

    has_more_latest = latest_hostels_qs.count() > 3
    has_more_more = more_hostels_qs.count() > 3

    context = {
        "latest_hostels": latest_hostels,
        "more_hostels": more_hostels,
        "categories": categories,
        "locations": locations,
        "query": query,
        "has_more_latest": has_more_latest,
        "has_more_more": has_more_more,
    }
    return render(request, "core/home.html", context)


def all_hostel_view(request):
    now = timezone.now()
    three_days_ago = now - timedelta(days=3)

    hostel_type = request.GET.get("type", "latest")

    categories = Hostel.CATEGORY_CHOICES
    locations = Hostel.objects.values_list("location", flat=True).distinct()
    query = request.GET.get("q", "")

    if hostel_type == "latest":
        hostels_qs = Hostel.objects.filter(
            created_at__gte=three_days_ago, available_vacants__gt=0
        )
        page_title = "All Latest Hostels"
    else:
        hostels_qs = Hostel.objects.filter(
            created_at__lt=three_days_ago, available_vacants__gt=0
        )
        page_title = "All More Hostels"

    if query:
        search_filter = Q()
        query_words = query.split()
        price_numbers = re.findall(r"\d+", query)

        for word in query_words:
            word_filter = (
                Q(name__icontains=word)
                | Q(address__icontains=word)
                | Q(location__icontains=word)
                | Q(description__icontains=word)
            )

            for choice_key, choice_display in categories:
                if word.lower() in choice_display.lower():
                    word_filter |= Q(category=choice_key)

            search_filter &= word_filter

        if price_numbers:
            price_filter = Q()
            for price_str in price_numbers:
                price_value = int(price_str)
                price_filter |= Q(
                    pricing__gte=price_value - 500, pricing__lte=price_value + 500
                )
            search_filter &= price_filter

        hostels_qs = hostels_qs.filter(search_filter)

    hostels = hostels_qs.order_by("-created_at")

    context = {
        "hostels": hostels,
        "categories": categories,
        "locations": locations,
        "query": query,
        "hostel_type": hostel_type,
        "page_title": page_title,
    }

    return render(request, "core/all_hostels.html", context)


@csrf_exempt
@require_http_methods(["POST"])
def submit_property_listing(request):
    try:
        data = json.loads(request.body)

        required_fields = ["name", "contact", "role", "area", "rent"]
        for field in required_fields:
            if not data.get(field):
                return JsonResponse(
                    {"status": "error", "message": f"{field} is required"}, status=400
                )

        property_listing = PropertyListing.objects.create(
            name=data["name"],
            contact=data["contact"],
            role=data["role"],
            area=data["area"],
            rent=data["rent"],
            hostel=data.get("hostel", ""),
        )

        return JsonResponse(
            {
                "status": "success",
                "message": "Property listing submitted successfully",
                "listing_id": property_listing.id,
            }
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"status": "error", "message": "Invalid JSON data"}, status=400
        )

    except Exception:
        return JsonResponse(
            {
                "status": "error",
                "message": "An error occurred while processing your request",
            },
            status=500,
        )


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
