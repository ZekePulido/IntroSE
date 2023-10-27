from django.shortcuts import render, redirect
from .forms import RegisterForm, ProfileUpdateForm, UpdateUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.
def home(request):
    return render(request, 'Main/home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            profile = Profile(user=user)
            profile.save()

            return redirect('/home')
    else:
        form = RegisterForm()


    return render(request, 'registration/register.html', {"form": form})


def dashboard(request):
    userprofile = Profile.objects.get(user=request.user)
    context = {
        'userprofile': userprofile,
    }
    return render(request, 'Main/dashboard.html', context)

@login_required
def profile(request):
    userprofile = Profile.objects.get(user=request.user)
    context = {
        'userprofile': userprofile,
    }
    return render(request, 'Main/profile.html',context)

@login_required
def profile_update(request):
    user = request.user
    profile_user = request.user.profile
    

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Update user information
            profile_form.save()  # Update profile information
            messages.success(request, 'Your profile was successfully updated.')
            return redirect('profile')
    else:
        user_form = UpdateUserForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile_user)

    return render(request, 'Main/profile_update.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

