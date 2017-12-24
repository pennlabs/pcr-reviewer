from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.http import require_http_methods
from django.contrib import messages


def index(request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html")
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
