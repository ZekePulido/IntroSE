from django.shortcuts import render, redirect
from .forms import RegisterForm, ProfileImageForm, UpdateProfileForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

@login_required
def profile(request):
    # Fetch the current user's profile
    profile_user = UserProfile.objects.get(user__id=request.user.id)
    edit_mode = 'edit' in request.GET

    if edit_mode:
        if request.method == 'POST':
            update_form = UpdateProfileForm(request.POST, instance=request.user)
            profile_form = ProfileImageForm(request.POST, request.FILES, instance=profile_user)

            if update_form.is_valid() and profile_form.is_valid():
                update_form.save()
                profile_form.save()

                # Notify user of update success
                messages.success(request, "Your profile was successfully updated.")

                # Clear all media files except current profile picture
                media_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
                current_picture = profile_form.instance.image.name

                for filename in media_storage.listdir('')[1]:
                    if filename != current_picture:
                        file_path = media_storage.url(filename)
                        media_storage.delete(file_path)

                return redirect('profile')

            else:
                messages.error(request, "There was an error updating your profile.")
        else:
            update_form = UpdateProfileForm(instance=request.user)
            profile_form = ProfileImageForm(instance=profile_user)
    else:
        update_form = None
        profile_form = ProfileImageForm(instance=profile_user)

    context = {
    'profile_form': profile_form,
    'edit_mode': edit_mode,
    'form': update_form,
    'profile_user': profile_user
    }

    return render(request, 'Main/profile.html', context)

