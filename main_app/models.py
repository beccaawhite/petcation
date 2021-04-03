from django.db import models

from django.contrib.auth.models import User
# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=True)
    is_sitter = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    pets = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=100)
    sit_count = models.IntegerField()
    pet_experience = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    

class Pet(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    characteristics = models.TextField(max_length=400)
    care_instructions = models.TextField(max_length=600)

    def __str__(self):
        return self.name

class Post(models.Model):
    start_date = models.DateField('start date')
    end_date = models.DateField('end date')
    details = models.TextField(max_length=600)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    def __str__(self):
        return self.details
