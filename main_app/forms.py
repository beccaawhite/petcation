from django.forms import ModelForm
from django import forms
from .models import Pet, Post, ShowInterest

class PetForm(ModelForm):
  class Meta:
    model = Pet
    fields = ['name', 'pet_type', 'breed', 'age', 'gender', 'characteristics', 'care_instructions']

class PostingForm(ModelForm):
  class Meta:
    model = Post
    fields = ['start_date', 'end_date','details'] 

class ShowInterestForm(forms.ModelForm):
  is_interested = forms.BooleanField()
  class Meta:
    model = ShowInterest
    fields = ['is_interested']

  def __init__(self, *args, **kwargs):
        super(ShowInterestForm, self).__init__(*args, **kwargs)
        self.fields['is_interested'].widget = forms.CheckboxSelectMultiple()
