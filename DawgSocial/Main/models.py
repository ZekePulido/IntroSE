from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image= models.ImageField(null = True, blank = True, upload_to='media/')

    def __str__(self):
        return self.user.username
