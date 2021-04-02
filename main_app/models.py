from django.db import models

from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=True)
    is_sitter = models.BooleanField(default=False)
    pets = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=100)
    sit_count = models.IntegerField()
    pet_experience = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=100)

