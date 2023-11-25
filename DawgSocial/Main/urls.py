from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('register',views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile', views.profile, name='profile'),
    path('profile_update', views.profile_update, name='profile_update'),
    path('create_post', views.create_post, name='create_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('share_post/<int:post_id>/', views.share_post, name='share_post'),
    path('share_post_u/<str:username>/<int:post_id>/', views.share_post_u, name='share_post_u'),
    path('friend_requests', views.friend_request, name = 'friend_request'),
    path('send_friend_request/<int:user_id>/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:requestID>/', views.accept_friend_request, name='accept_friend_request'),
    path('user_profile/<str:username>/<int:post_id>/', views.user_profile, name='user_profile_u'),
    path('user_profile/<str:username>/', views.user_profile, name='user_profile'),
    path('remove_friend/<str:friend_username>/', views.remove_friend, name='remove_friend'),
    path('like/<int:post_id>/', views.like, name='like'),
    path('like_u/<str:username>/<int:post_id>/', views.like_u, name='like_u'),
    path('post_comment/<int:post_id>/', views.post_comment, name='post_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('dislike/<int:post_id>/', views.dislike, name='dislike'),
    path('dislike_u/<str:username>/<int:post_id>/', views.dislike_u, name='dislike_u'),
    path('reject_friend_request/<int:requestID>/', views.reject_friend_request, name='reject_friend_request'),
    path('withdraw_friend_request/<int:requestID>/', views.withdraw_friend_request, name='withdraw_friend_request'),
    path('favorite/<int:post_id>/', views.favorite, name='favorite'),
    path('favorite_u/<str:username>/<int:post_id>/', views.favorite_u, name='favorite_u'),
    path('favorited_posts', views.favorited_posts, name='favorited_posts'),
    path('search/', views.user_search, name='user_search'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
