from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    birthday = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4}), label="Bio (optional)")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2','birthday','bio']


class ProfileImageForm(forms.ModelForm):
    image=forms.ImageField(label="Profile")
    class Meta:
        model = UserProfile  
        fields = ['image']

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    birthday = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4}), label="Bio (optional)")

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'birthday', 'bio']
