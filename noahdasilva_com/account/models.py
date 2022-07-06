from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to='user_profile_images/')
    instagram = models.URLField(max_length=255, null=True, blank=True)
    twitter = models.URLField(max_length=255, null=True, blank=True)
    linkedin = models.URLField(max_length=255, null=True, blank=True)
