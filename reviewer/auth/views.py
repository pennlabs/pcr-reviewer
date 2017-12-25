from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.conf import settings

from django.db.models import Count
from ..reviews.models import Section, Review


def index(request):
    if request.user.is_authenticated:
        context = {
            "reviewed": Section.objects.annotate(num_reviews=Count("review")).filter(num_reviews__gte=settings.REVIEWER_THRESHOLD).count(),
            "total": Section.objects.count(),
            "user_reviewed": Review.objects.filter(reviewer=request.user).count(),
            "reviews": Review.objects.filter(reviewer=request.user).order_by("-id")[:10]
        }

        return render(request, "dashboard.html", context)
    else:
        return render(request, "index.html")


@require_http_methods(["POST"])
def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
    else:
        messages.error(request, "Login attempt failed!")
    return redirect("index")


def logout(request):
    auth_logout(request)
    return redirect("index")
