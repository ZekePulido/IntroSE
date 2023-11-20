from django.shortcuts import render, redirect
from .forms import RegisterForm, ProfileUpdateForm, UpdateUserForm,PostForm, ShareForm, LikeForm, DisLikeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Profile, Friend_Request,Comment
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
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


@login_required
def dashboard(request):
    userprofile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(user__profile__friends=request.user).prefetch_related('comments')
    reposts = Post.objects.filter(shared_user=request.user).prefetch_related('comments')
    all_posts = (posts | reposts).distinct().order_by('-created_at')
    
    context = {
        'userprofile': userprofile,
        'posts': all_posts,
    }
    favorited_posts = Post.objects.filter(favorited_by=request.user)

    context = {
        'userprofile': userprofile,
        'posts': all_posts,
        'favorited_posts': favorited_posts,

    }
    return render(request, 'Main/dashboard.html', context)

@login_required
def profile(request):
    userprofile = Profile.objects.get(user=request.user)
    user_posts = Post.objects.filter(user=request.user).prefetch_related('comments') # Fetch the user's posts
 # Fetch the user's posts

    context = {
        'userprofile': userprofile,
        'user_posts': user_posts,  # Add user's posts to the context
    }
    return render(request, 'Main/profile.html', context)


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

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)      # post = form.save(commit=False)
            post.user = request.user # modify the post objec before saving it 
            post.save()
            messages.success(request, 'You have successfully created a post')
            return redirect('profile')
    else:
        form = PostForm()
    
    return render(request, 'Main/create_post.html', {'form': form})

    
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id = post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post.save()
            messages.success(request, 'Your post was successfully updated.')
            return redirect('profile')
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
            return redirect('profile')
        elif choice == 'no':
            return redirect('profile')
    
    return render(request, 'Main/delete_post.html', {'post':post})

@login_required
def send_friend_request(request, user_id):
    to_user = User.objects.get(id=user_id)
    from_user = request.user
    if to_user != from_user:
        friend_request, created = Friend_Request.objects.get_or_create(
            from_user=from_user, to_user=to_user
        )
        if created:
            messages.success(request, 'Friend request sent successfully.')
        else:
            messages.info(request, 'Friend request already sent.')


    return redirect('accept_page')


@login_required
def  accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.profile.friends.add(friend_request.from_user)
        friend_request.from_user.profile.friends.add(friend_request.to_user)
        friend_request.delete()
        messages.success(request, 'Friend request accepted')
    else:
        messages.error(request, 'Friend request not accepted')

    return redirect('accept_page')

@login_required
def remove_friend(request, friend_username):
    if request.user.is_authenticated:
        try:
            friend = User.objects.get(username=friend_username)
            request.user.profile.friends.remove(friend)
        except User.DoesNotExist:
            pass 
    return redirect('accept_page')

@login_required
def reject_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.delete()
        messages.success(request, 'Friend request rejected')
    else:
        messages.error(request, 'Friend request not rejected')

    return redirect('accept_page')


@login_required
def withdraw_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.from_user == request.user:
        friend_request.delete()
        messages.success(request, 'Friend request withdrawn')
    else:
        messages.error(request, 'Friend request not withdrawn')

    return redirect('accept_page')


@login_required
def viewing_page(request):
    friends = request.user.profile.friends.all()
    allusers = User.objects.exclude(Q(id=request.user.id) | Q(id__in=friends))

    context = {
        'allusers': allusers,
    }
    return render(request, 'Main/all_users.html', context)

@login_required
def accept_page(request):
    friends = request.user.profile.friends.all()
    friend_requests_received = Friend_Request.objects.filter(to_user=request.user)
    friend_requests_sent = Friend_Request.objects.filter(from_user=request.user)
    allusers = User.objects.exclude(Q(id=request.user.id) | Q(id__in=friends) | Q(id__in=friend_requests_received.values('from_user')))

    context = {
        'allusers': allusers,
        'friends': friends,
        'friend_requests_received': friend_requests_received,
        'friend_requests_sent': friend_requests_sent,
    }

    for friend_request in friend_requests_received:
        if friend_request.from_user in friends:
            friend_request.delete()

    return render(request, 'Main/accept_users.html', context)

@login_required
def user_profile(request, username, post_id=None):
    friend = get_object_or_404(User, username=username)
    friend_posts = Post.objects.filter(user=friend).prefetch_related('comments')
    
    # Add a can_comment flag to each post
    for post in friend_posts:
        post.can_comment = request.user.profile.friends.filter(id=post.user.id).exists()

    context = {
        'friend': friend,
        'friend_posts': friend_posts,
    }
    return render(request, 'Main/user_profile.html', context)

@csrf_protect
@login_required
def like(request, post_id=None):
    if request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            user = request.user
            post_id = form.cleaned_data['post_id']
            post = Post.objects.get(id=post_id)

            liked = post.liked_by.filter(id=user.id).exists()
            disliked = post.disliked_by.filter(id=user.id).exists()

            if liked:
                post.liked_by.remove(user)
            else:
                post.liked_by.add(user)

                # If the user has already disliked the post, remove the dislike
                if disliked:
                    post.disliked_by.remove(user)

            like_count = post.liked_by.count()

            return redirect('dashboard')  # Redirect to the dashboard after the like is processed

    return redirect('dashboard')

@csrf_protect
@login_required
def like_u(request, username, post_id=None):
    friend = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            user = request.user
            post_id = form.cleaned_data['post_id']
            post = Post.objects.get(id=post_id)

            liked = post.liked_by.filter(id=user.id).exists()
            disliked = post.disliked_by.filter(id=user.id).exists()

            if liked:
                post.liked_by.remove(user)
            else:
                post.liked_by.add(user)

                # If the user has already disliked the post, remove the dislike
                if disliked:
                    post.disliked_by.remove(user)

            like_count = post.liked_by.count()

            # Include the post_id parameter in the redirect
            return redirect('user_profile_u', username=friend.username, post_id=post_id)

    # Include the post_id parameter in the redirect
    return redirect('user_profile_u', username=friend.username, post_id=post_id)



@csrf_protect
@login_required
def share_post(request, post_id):
    original_post = get_object_or_404(Post, id=post_id)
    #Allow repost once
    if Post.objects.filter(shared_user=original_post.user, user=request.user).exists():
        messages.error(request, "You have already shared this post.")
        print("You have already shared this post.")
        return redirect('dashboard')
    if request.user.profile.friends.filter(id=original_post.user.id).exists():
        if request.method == 'POST':
            form = ShareForm(request.POST)
            if form.is_valid():
                shared_caption = form.cleaned_data.get('caption', '')

                new_post = Post(
                    content = original_post.content,
                    shared_caption=shared_caption,
                    caption=original_post.caption,
                    user=request.user,
                    shared_user=original_post.user
                )
                new_post.save()

                return redirect('dashboard')

        else:
            form = ShareForm(initial={'post_id':post_id})

    return render(request, 'Main/share_post.html', {'form': form, 'post_id': post_id})

@csrf_protect
@login_required
def share_post_u(request,username, post_id):
    friend = get_object_or_404(User, username=username)
    original_post = get_object_or_404(Post, id=post_id)
    #Allow repost once
    if Post.objects.filter(shared_user=original_post.user, user=request.user).exists():
        messages.error(request, "You have already shared this post.")
        print("You have already shared this post.")
        return redirect('user_profile_u', username=friend.username, post_id=post_id)
    if request.user.profile.friends.filter(id=original_post.user.id).exists():
        if request.method == 'POST':
            form = ShareForm(request.POST)
            if form.is_valid():
                shared_caption = form.cleaned_data.get('caption', '')

                new_post = Post(
                    content = original_post.content,
                    shared_caption=shared_caption,
                    caption=original_post.caption,
                    user=request.user,
                    shared_user=original_post.user
                )
                new_post.save()

                return redirect('user_profile_u', username=friend.username, post_id=post_id)

        else:
            form = ShareForm(initial={'post_id':post_id})

    return render(request, 'Main/share_post.html', {'form': form, 'post_id': post_id})

@login_required
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Check if the user is a friend of the post's author
    if request.user.profile.friends.filter(id=post.user.id).exists():
        if request.method == 'POST':
            comment_content = request.POST.get('comment_content')
            Comment.objects.create(user=request.user, post=post, content=comment_content)
            messages.success(request, 'Your comment was successfully added.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'dashboard'))
    else:
        messages.error(request, 'You can only comment on friends\' posts.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'dashboard'))

@csrf_protect
@login_required
def dislike(request, post_id=None):
    if request.method == 'POST':
        form = DisLikeForm(request.POST)
        if form.is_valid():
            user = request.user
            post_id = form.cleaned_data['post_id']
            post = Post.objects.get(id=post_id)

            disliked = post.disliked_by.filter(id=user.id).exists()
            liked = post.liked_by.filter(id=user.id).exists()

            if disliked:
                post.disliked_by.remove(user)
            else:
                post.disliked_by.add(user)

                # If the user has already liked the post, remove the like
                if liked:
                    post.liked_by.remove(user)

            dislike_count = post.disliked_by.count()

            return redirect('dashboard')  # Redirect to the dashboard after the dislike is processed

    return redirect('dashboard')

@csrf_protect
@login_required
def dislike_u(request,username, post_id=None):
    friend = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = DisLikeForm(request.POST)
        if form.is_valid():
            user = request.user
            post_id = form.cleaned_data['post_id']
            post = Post.objects.get(id=post_id)

            disliked = post.disliked_by.filter(id=user.id).exists()
            liked = post.liked_by.filter(id=user.id).exists()

            if disliked:
                post.disliked_by.remove(user)
            else:
                post.disliked_by.add(user)

                # If the user has already liked the post, remove the like
                if liked:
                    post.liked_by.remove(user)

            dislike_count = post.disliked_by.count()

            return redirect('user_profile_u',username=friend.username, post_id=post_id) 

    return redirect('user_profile_u',username=friend.username, post_id=post_id)

@login_required
def favorite(request, post_id=None):
    if request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            user = request.user
            post_id = form.cleaned_data['post_id']
            post = Post.objects.get(id=post_id)

            favorited = post.favorited_by.filter(id=user.id).exists()

            if favorited:
                post.favorited_by.remove(user)
            else:
                post.favorited_by.add(user)

            return redirect('dashboard')  # Redirect to the dashboard after the favorite is processed

    return redirect('dashboard')

@login_required
def favorite_u(request, username, post_id=None):
    friend = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            user = request.user
            post_id = form.cleaned_data['post_id']
            post = Post.objects.get(id=post_id)

            favorited = post.favorited_by.filter(id=user.id).exists()

            if favorited:
                post.favorited_by.remove(user)
            else:
                post.favorited_by.add(user)

            return redirect('user_profile_u',username=friend.username, post_id=post_id) 

    return redirect('user_profile_u',username=friend.username, post_id=post_id) 

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Your comment was successfully deleted.')
        return redirect('dashboard')  # Redirect to the dashboard or relevant page
    return render(request, 'Main/delete_comment.html', {'comment': comment})

@login_required
def favorited_posts(request):
    favorited_posts = Post.objects.filter(favorited_by=request.user)

    context = {
        'favorited_posts': favorited_posts,
    }
    return render(request, 'Main/favorited_posts.html', context)
