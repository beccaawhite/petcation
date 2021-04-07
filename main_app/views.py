from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Owner, Sitter, Pet, Post, Photo, SitterPhoto, SitterProfile, OwnerProfile
from .forms import PetForm,PostingForm, ShowInterestForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

import uuid
import boto3
# S3_BASE_URL ='https://s3.us-west-1.amazonaws.com/'
# BUCKET = 'beccaabucket'
# S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
# BUCKET = 'atusacatcollector'
S3_BASE_URL = 'https://s3.us-west-2.amazonaws.com/'
BUCKET = 'ninascats'


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


# Owner Views
class OwnerCreate(CreateView):
  model = Owner
  fields = ['first_name', 'last_name', 'city', 'about']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class OwnerUpdate(UpdateView):
  model = Owner
  fields = ['first_name', 'last_name', 'city', 'about']

class OwnerDelete(DeleteView):
  model = Owner
  success_url = '/'

def owners_detail(request, owner_id):
  owner = Owner.objects.get(id=owner_id)
  return render(request, 'owners/detail.html', {
    'owner': owner,
  })

def pets_create(request, owner_id):
  owner = Owner.objects.get(id=owner_id)
  pet_form = PetForm()
  return render(request, 'owners/pet_form.html', {
    'owner': owner,
    'pet_form': pet_form
  })

def owners_index(request):
  owners = Owner.objects.filter(user=request.user)
  return render(request, 'owners/index.html', { 'owners': owners })

def add_pet(request, owner_id):
  # create the PetForm using data in request.POST
  form = PetForm(request.POST)
  # validate form
  if form.is_valid():
    # don't save the form to the db until is has the owner_id assigned
    new_pet = form.save(commit=False)
    new_pet.owner_id = owner_id
    new_pet.save()
  return redirect('owners_detail', owner_id=owner_id)

# Pet Views
def pets_detail(request, pet_id):
  pet = Pet.objects.get(id=pet_id)
  return render(request, 'owners/pets/detail.html', {
    'pet': pet
  })

class PetUpdate(UpdateView):
  model = Pet
  fields = ['name', 'pet_type', 'breed', 'age', 'gender', 'characteristics', 'care_instructions']

class PetDelete(DeleteView):
  model = Pet
  success_url = '/owners/{owner_id}/'

# Sitter Views
class SitterCreate(CreateView):
  model = Sitter

  fields = ['first_name', 'last_name', 'city', 'pet_experience', 'about']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class SitterUpdate(UpdateView):
  model = Sitter
  fields = ['first_name', 'last_name', 'city', 'pet_experience', 'about']

class SitterDelete(DeleteView):
  model = Sitter
  success_url = '/'


def sitters_detail(request, sitter_id):
  sitter = Sitter.objects.get(id=sitter_id)
  return render(request, 'sitters/detail.html', {
    'sitter': sitter
  })

def sitters_index(request):
  sitters = Sitter.objects.filter(user=request.user)
  return render(request, 'sitters/index.html', { 'sitters': sitters })

#adds photos of pets to owners profile 
def add_photo(request, owner_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    # print(photo_file, "pphoto file")
    if photo_file:
        s3 = boto3.client('s3')
        print(s3, "S3")
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        print(key, "KEY!")
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            print(url)
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, owner_id=owner_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('owners_detail', owner_id=owner_id)

#adds owner profile picture
def add_owner_profile(request, owner_id):
    photo_file = request.FILES.get('photo-file', None)
    # print(photo_file, "pphoto file")
    if photo_file:
        s3 = boto3.client('s3')
        print(s3, "S3")
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        print(key, "KEY!")
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            print(url, "URL!!!!")
            OwnerProfile.objects.create(url=url, owner_id=owner_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('owners_detail', owner_id=owner_id)


def add_sitter_profile(request, sitter_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        print(s3, "S3")
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        print(key, "KEY!")
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            print(url, "URL!!!!!!!!!")
            SitterPhoto.objects.create(url=url, sitter_id=sitter_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('sitters_detail', sitter_id=sitter_id)


def add_sitter_photo(request, sitter_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        print(s3, "S3")
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        print(key, "KEY!")
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            print(url, "URL!!!!!!!!!")
            SitterProfile.objects.create(url=url, sitter_id=sitter_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('sitters_detail', sitter_id=sitter_id)



#creating post by owner
def posts_create(request, owner_id):
      owner = Owner.objects.get(id=owner_id)
      post_form = PostingForm()
      return render(request, 'owners/post_form.html', {
        'owner': owner,
        'post_form': post_form
      })

#adding post by owner
def add_posting(request, owner_id):
      	
  form = PostingForm(request.POST)
  # validate the form
  if form.is_valid():
    new_posting = form.save(commit=False)
    new_posting.owner_id = owner_id
    new_posting.save()
  # return redirect('detail', owner_id=owner_id)
  return redirect('index')

  
# pots list
def posts_index(request):
  posts = Post.objects.all() 
  return render(request, 'posts/index.html', { 
    'posts': posts,    
  })

def posts_detail(request, post_id):
  # sitter = Sitter.objects.get(id=sitter_id)
  post = Post.objects.get(id=post_id)
  
  show_interest_form = ShowInterestForm()
  return render(request, 'posts/detail.html', {
    'post': post,
    'show_interest_form': show_interest_form,
  })

def show_interest(request, post_id):
  print(request.user.id, ' THIS IS REQ.USER')
  form = ShowInterestForm(request.POST)
  if form.is_valid():
    show_interest = form.save(commit=False)
    show_interest.post_id = post_id
    show_interest.sitter_id = request.user.id
    show_interest.save()
  return redirect(request, 'posts_detail', post_id=post_id)

class PostUpdate(UpdateView):
  model = Post
  fields = ['start_date', 'end_date', 'details']

class PostDelete(DeleteView):
  model = Post
  success_url = '/posts/'