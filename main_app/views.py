from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Owner, Sitter, Pet, Post, Photo

# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

import uuid
import boto3
S3_BASE_URL ='https://s3.us-west-1.amazonaws.com/'
BUCKET = 'beccaabucket'

# Define the home view
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class OwnerCreate(CreateView):
  model = Owner
  fields = ['first_name', 'last_name', 'city', 'about']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

def owners_detail(request, owner_id):
  owner = Owner.objects.get(id=owner_id)
  return render(request, 'owners/detail.html', {
    'owner': owner
  })

def owners_index(request):
  owners = Owner.objects.filter(user=request.user)
  return render(request, 'owners/index.html', { 'owners': owners })

class SitterCreate(CreateView):
  model = Sitter
  fields = ['first_name', 'last_name', 'city', 'pet_experience', 'about']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

def sitters_detail(request, sitter_id):
  sitter = Sitter.objects.get(id=sitter_id)
  return render(request, 'sitters/detail.html', {
    'sitter': sitter
  })

def sitters_index(request):
  sitters = Sitter.objects.filter(user=request.user)
  return render(request, 'sitters/index.html', { 'sitters': sitters })


def add_photo(request, sitter_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            print(url)
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, sitter_pic_id=sitter_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', sitter_id=sitter_id)