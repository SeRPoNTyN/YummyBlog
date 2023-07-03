import django.forms
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import *
from .forms import *


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = UserLoginForm()
    return render(request, "blog/login.html", {'form': form})


def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserRegisterForm()
    return render(request, "blog/register.html", {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data["subject"], form.cleaned_data["content"], "nector16@mail.ru", ["serpontynfunny@mail.ru"], fail_silently=False)
            if mail:
                messages.success(request, "Письмо отправлено!")
                return redirect("home")
            else:
                messages.error(request, "Ошибка отправки.")
                return redirect("contact")
        else:
            messages.error(request, "Ошибка валидации.")
    else:
        form = ContactForm()
    return render(request, "blog/contact.html", {"form": form})