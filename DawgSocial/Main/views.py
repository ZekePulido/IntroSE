from django.shortcuts import render, redirect
from .forms import RegisterForm, ProfileImageForm
from django.contrib.auth import login, logout, authenticate
from .models import UserProfile
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

            profile = UserProfile(user=user)
            profile.save()

            return redirect('/home')
    else:
        form = RegisterForm()


    return render(request, 'registration/register.html', {"form": form})


def dashboard(request):
    userprofile = UserProfile.objects.get(user=request.user)
    context = {
        'userprofile': userprofile,
    }
    return render(request, 'Main/dashboard.html', context)

def profile(request):
    # Fetch the current user's profile
    profile_user = UserProfile.objects.get(user__id=request.user.id)

    if request.user.is_authenticated:
        if request.method == 'POST':
            profile_form = ProfileImageForm(request.POST, request.FILES, instance=profile_user)
            if profile_form.is_valid():
                profile_form.save()
                
                # Code to clear all media files except the current picture
                media_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
                current_picture = profile_form.instance.image.name

                for filename in media_storage.listdir('')[1]:
                    if filename != current_picture:
                        file_path = media_storage.url(filename)
                        media_storage.delete(file_path)

                return redirect('profile')
        else:
            profile_form = ProfileImageForm(instance=profile_user)
    else:
        return redirect('home')

    return render(request, 'Main/profile.html', {'profile_form': profile_form})
