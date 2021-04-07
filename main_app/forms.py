from django.forms import ModelForm
# from django import forms
from .models import Pet, Post, ShowInterest


class PetForm(ModelForm):
  class Meta:
    model = Pet
    fields = ['name', 'pet_type', 'breed', 'age', 'gender', 'characteristics', 'care_instructions']

class PostingForm(ModelForm):
  class Meta:
    model = Post
    fields = ['start_date', 'end_date','details'] 

class ShowInterestForm(ModelForm):
  class Meta:
    model = ShowInterest
    fields = ['is_interested']

