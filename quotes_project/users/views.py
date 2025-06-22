from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from ..users.forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("main")
        else:
            form = LoginForm()
        return render(request, "login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("main")
