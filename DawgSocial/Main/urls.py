from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('register',views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile', views.profile, name='profile')

]