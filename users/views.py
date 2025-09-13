from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    return render(request, "users/dashboard.html")


@login_required
def profile(request):
    return render(request, "users/profile.html")


@login_required
def favorites(request):
    return render(request, "users/favorites.html")


@login_required
def roomie_profile(request):
    return render(request, "users/roomie_profile.html")
