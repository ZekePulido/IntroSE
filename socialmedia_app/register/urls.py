from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='templates/login'),
    path('register/', views.register, name='template/register')
    # Add other URL patterns as needed
]