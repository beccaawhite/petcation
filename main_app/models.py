from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User
# Create your models here.



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
        return reverse('detail', kwargs={'owner_id': self.id})


class Sitter(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    about = models.TextField(max_length=600)
    sit_count = models.IntegerField(null=True)
    pet_experience = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'sitter_id': self.id})

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
        return reverse('detail', kwargs={'pet_id': self.id})

class Post(models.Model):
    start_date = models.DateField('start date')
    end_date = models.DateField('end date')
    details = models.TextField(max_length=600)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.details

 
class Photo(models.Model):
    url = models.CharField(max_length=200)
    sitter_pic = models.ForeignKey(Sitter, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for sitter_id: {self.sitter_id} @{self.url}"