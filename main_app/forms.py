from django.forms import ModelForm
# from django import forms
from .models import Pet, Post, ShowInterest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2' )


# IS_INTERESTED = ['Yes', 'No']

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

