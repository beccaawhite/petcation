from django.forms import ModelForm
from .models import Pet,Post

class PetForm(ModelForm):
  class Meta:
    model = Pet
    fields = ['name', 'pet_type', 'breed', 'age', 'gender', 'characteristics', 'care_instructions']

class PostingForm(ModelForm):
      class Meta:
        model = Post
        fields = ['start_date', 'end_date','details'] 

