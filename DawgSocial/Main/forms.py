from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Post

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birthday', 'bio','image']

class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class PostForm(forms.ModelForm):
    caption =forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Say something...'}))

    class Meta:
        model = Post
        fields = ['content', 'caption']
        widgets= {
            'content': forms.FileInput(attrs={'accept': 'image/*,video/*'})
        }

class ShareForm(forms.ModelForm):
    caption = forms.CharField(label= '', widget=forms.Textarea(attrs={'placeholder': 'Say something...'}))

class LikeForm(forms.Form):
    post_id = forms.IntegerField()


class DisLikeForm(forms.Form):
    post_id = forms.IntegerField()

