from django.shortcuts import render, redirect
from .forms import RegisterForm, ProfileUpdateForm, UpdateUserForm,PostForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Profile
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
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

    posts = Post.objects.all
    context = {
        'userprofile': userprofile,
        'posts': posts
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

@login_required
def create_post(request):
    print(request.user.is_authenticated)
    print(request.user.username)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)      # post = form.save(commit=False)
            post.user = request.user # modify the post objec before saving it 
            post.save()
            messages.success(request, 'You have successfully created a post')
            return redirect('dashboard')
    else:
        form = PostForm()
    
    return render(request, 'Main/create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    print(f"Post ID: {post_id}")
    post = get_object_or_404(Post, id = post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            #post.content = form.cleaned_data['content']
            #post.caption = form.cleaned_data['caption']
            post.save()
            messages.success(request, 'Your post was successfully updated.')
            return redirect('dashboard')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'Main/edit_post.html', {'form':form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        choice = request.POST.get('delete_choice')
        if choice == 'yes':
            post.delete()
            messages.success(request, 'Your post was successfully deleted.')
            return redirect('dashboard')
        elif choice == 'no':
            return redirect('dashboard')
    
    return render(request, 'Main/delete_post.html', {'post':post})
