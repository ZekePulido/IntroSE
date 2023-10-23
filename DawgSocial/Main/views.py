from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate


# Create your views here.
def home(request):
    return render(request, 'Main/home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()


    return render(request, 'registration/register.html', {"form": form})


def dashboard(request):
    return render(request, 'Main/dashboard.html')

def profile(request):
    return render(request,'Main/profile.html')