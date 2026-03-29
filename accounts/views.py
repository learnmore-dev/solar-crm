from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# ---------------- LOGIN ----------------
def login_view(request):

    # If already logged in
    if request.user.is_authenticated:
        return redirect('leads:dashboard')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('leads:dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    return redirect("login")