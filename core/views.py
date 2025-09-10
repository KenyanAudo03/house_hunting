from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from .models import Hostel, PropertyListing
import re
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.http import require_http_methods
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    query = request.GET.get("q", "")

    if query:
        return redirect(f"/all-hostels/?type=search&q={query}")

    now = timezone.now()
    five_days_ago = now - timedelta(days=5)

    # Latest (5 days) - all categories
    latest_hostels_qs = Hostel.objects.filter(
        created_at__gte=five_days_ago, available_vacants__gt=0
    ).order_by("-created_at")

    # Single rooms only
    single_hostels_qs = Hostel.objects.filter(
        category="single", available_vacants__gt=0
    ).order_by("-created_at")

    # Bedsitter + 1-bedroom + 2-bedroom
    bedsitter_bedroom_qs = Hostel.objects.filter(
        category__in=["bedsitter", "one_bedroom", "two_bedroom"],
        available_vacants__gt=0,
    ).order_by("-created_at")

    latest_hostels = latest_hostels_qs[:15]
    single_hostels = single_hostels_qs[:15]
    bedsitter_bedroom_hostels = bedsitter_bedroom_qs[:15]

    # Show "View All" if more than 4 exist
    has_more_latest = latest_hostels_qs.count() > 4
    has_more_single = single_hostels_qs.count() > 4
    has_more_bedsitter_bedroom = bedsitter_bedroom_qs.count() > 4

    context = {
        "latest_hostels": latest_hostels,
        "single_hostels": single_hostels,
        "bedsitter_bedroom_hostels": bedsitter_bedroom_hostels,
        "query": query,
        "has_more_latest": has_more_latest,
        "has_more_single": has_more_single,
        "has_more_bedsitter_bedroom": has_more_bedsitter_bedroom,
    }
    return render(request, "core/home.html", context)


def all_hostel_view(request):
    hostel_type = request.GET.get("type", "latest")
    categories = Hostel.CATEGORY_CHOICES
    query = request.GET.get("q", "")
    page_number = request.GET.get("page", 1)

    now = timezone.now()
    five_days_ago = now - timedelta(days=5)

    # Select queryset by hostel type
    if hostel_type == "latest":
        hostels_qs = Hostel.objects.filter(
            created_at__gte=five_days_ago, available_vacants__gt=0
        )
        base_title = "Latest Hostels"

    elif hostel_type == "single":
        hostels_qs = Hostel.objects.filter(category="single", available_vacants__gt=0)
        base_title = "Single Room Hostels"

    elif hostel_type == "bedsitter_bedroom":
        hostels_qs = Hostel.objects.filter(
            category__in=["bedsitter", "one_bedroom", "two_bedroom"],
            available_vacants__gt=0,
        )
        base_title = "Bedsitters & Bedrooms"

    elif hostel_type == "search":
        hostels_qs = Hostel.objects.filter(available_vacants__gt=0)
        base_title = "Search Results"

    else:  # fallback
        hostels_qs = Hostel.objects.filter(
            created_at__gte=five_days_ago, available_vacants__gt=0
        )
        base_title = "Latest Hostels"

    # Apply search if query exists
    if query:
        search_filter = Q()
        query_words = query.split()

        for word in query_words:
            word_filter = (
                Q(name__icontains=word)
                | Q(address__icontains=word)
                | Q(location__icontains=word)
                | Q(description__icontains=word)
            )

            if word.isdigit():  # Match numeric query to price range
                price_value = int(word)
                word_filter |= Q(
                    pricing__gte=price_value - 500, pricing__lte=price_value + 500
                )

            for choice_key, choice_display in categories:
                if word.lower() in choice_display.lower():
                    word_filter |= Q(category=choice_key)

            search_filter &= word_filter

        hostels_qs = hostels_qs.filter(search_filter)

    hostels_qs = hostels_qs.order_by("-created_at")
    total_results = hostels_qs.count()

    # Pagination
    paginator = Paginator(hostels_qs, 10)
    try:
        hostels = paginator.page(page_number)
    except PageNotAnInteger:
        hostels = paginator.page(1)
    except EmptyPage:
        hostels = paginator.page(paginator.num_pages)

    page_title = (
        f"Search Results for '{query}'"
        if hostel_type == "search" and query
        else base_title
    )

    context = {
        "hostels": hostels,
        "query": query,
        "hostel_type": hostel_type,
        "page_title": page_title,
        "total_results": total_results,
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
