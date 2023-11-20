from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name='user_friends')
    image = models.ImageField(null=True, blank=True, upload_to='media/')
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    content = models.ImageField(null=True, blank=True, upload_to='media/')
    caption = models.TextField(null=True, blank=True)
    shared_caption = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shared_at = models.DateTimeField(auto_now_add=True)  # Use auto_now_add for the initial shared time
    liked_by = models.ManyToManyField(User, related_name='liked_posts')
    disliked_by = models.ManyToManyField(User, related_name='disliked_posts')

    class Meta:
        ordering = ['-created_at', '-shared_at']
        
    caption = models.TextField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(limit_value=255, message="Caption must be at most 255 characters.")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(User,related_name='liked_posts')
    disliked_by= models.ManyToManyField(User,related_name='disliked_posts')
    favorited_by = models.ManyToManyField(User, related_name='favorited_posts', blank=True)

    def total_likes(self):
        return self.liked_by.count()

    def __str__(self):
        return f'{self.user.username} - {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'

    
class Friend_Request(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'
