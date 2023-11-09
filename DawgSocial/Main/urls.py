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
    path('accept_page', views.accept_page, name = 'accept_page'),
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:requestID>/', views.accept_friend_request, name='accept_friend_request'),
    path('user_profile/<str:username>/', views.user_profile, name='user_profile'),
    path('remove_friend/<str:friend_username>/', views.remove_friend, name='remove_friend'),
    path('like/<int:post_id>/', views.like, name='like'),
    path('post_comment/<int:post_id>/', post_comment, name='post_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
