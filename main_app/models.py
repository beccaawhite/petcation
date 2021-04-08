from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User

IS_INTERESTED = (
    ('Y', 'Yes'),
    ('N', 'No')
)

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    about = models.TextField(max_length=600)
    pets = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('owners_detail', kwargs={'owner_id': self.id})


class Sitter(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    about = models.TextField(max_length=600)
    sit_count = models.IntegerField(null=True)
    pet_experience = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('sitters_detail', kwargs={'sitter_id': self.id})


class Pet(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    characteristics = models.TextField(max_length=400)
    care_instructions = models.TextField(max_length=600)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('pets_detail', kwargs={'pet_id': self.id})

class Post(models.Model):
    start_date = models.DateField('start date')
    end_date = models.DateField('end date')
    details = models.TextField(max_length=600)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    sitters = models.ManyToManyField(Sitter)

    def __str__(self):
        return self.details

    def get_absolute_url(self):
        return reverse('posts_detail', kwargs={'post_id': self.id})

class ShowInterest(models.Model):
    sitter = models.ForeignKey(Sitter, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_interested = models.CharField(
        max_length=1,
        choices=IS_INTERESTED,
        default=IS_INTERESTED[0][1]
    )

    def __str__(self):
        return f"{self.get_is_interested_display()}"

# owners can post pet photos on bottom of their profile
class Photo(models.Model):
    url = models.CharField(max_length=200)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for owner_id: {self.owner_id} @{self.url}"

# sitters profile picture
class SitterPhoto(models.Model): 
    url = models.CharField(max_length=200)
    sitter = models.ForeignKey(Sitter, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for sitter_id: {self.sitter_id} @{self.url}"

# class that hold the sitter profile picture
class SitterProfile(models.Model): 
    url = models.CharField(max_length=200)
    sitter = models.ForeignKey(Sitter, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for sitter_id: {self.sitter_id} @{self.url}"

# owners profile picture
class OwnerProfile(models.Model):
    url = models.CharField(max_length=200)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for owner_id: {self.owner_id} @{self.url}"
