from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Owner, Sitter, Pet, Post, Photo, SitterPhoto, SitterProfile, OwnerProfile
from .forms import PetForm,PostingForm, ShowInterestForm, SignUpForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid
import boto3
import os

# S3_BASE_URL ='https://s3.us-west-1.amazonaws.com/'
# BUCKET = 'beccaabucket'
# S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
# BUCKET = 'atusacatcollector'
S3_BASE_URL = 'https://s3.us-west-2.amazonaws.com/'
BUCKET = 'ninascats'

# S3_BASE_URL ='https://s3.us-west-1.amazonaws.com/'
# BUCKET = 'beccaabucket'

# Home and signup views
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    # form = UserCreationForm(request.POST)
    form = SignUpForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = SignUpForm()
  context = {'form': form, 'error_message': error_message}
  print(context, 'this is context')
  return render(request, 'registration/signup.html', context)


# Owner Views
class OwnerCreate(LoginRequiredMixin, CreateView):
  model = Owner
  fields = ['first_name', 'last_name', 'city', 'about']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class OwnerUpdate(LoginRequiredMixin, UpdateView):
  model = Owner
  fields = ['first_name', 'last_name', 'city', 'about']

class OwnerDelete(LoginRequiredMixin, DeleteView):
  model = Owner
  success_url = '/'

@login_required
def owners_detail(request, owner_id):
  my_key = os.environ['SECRET_KEY']
  owner = Owner.objects.get(id=owner_id)
  return render(request, 'owners/detail.html', {
    'owner': owner,
  })

@login_required
def pets_create(request, owner_id):
  owner = Owner.objects.get(id=owner_id)
  pet_form = PetForm()
  return render(request, 'owners/pet_form.html', {
    'owner': owner,
    'pet_form': pet_form
  })

@login_required
def owners_index(request):
  owners = Owner.objects.filter(user=request.user)
  return render(request, 'owners/index.html', { 'owners': owners })

@login_required
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
@login_required
def pets_detail(request, pet_id):
  pet = Pet.objects.get(id=pet_id)
  return render(request, 'owners/pets/detail.html', {
    'pet': pet
  })

class PetUpdate(LoginRequiredMixin, UpdateView):
  model = Pet
  fields = ['name', 'pet_type', 'breed', 'age', 'gender', 'characteristics', 'care_instructions']

class PetDelete(LoginRequiredMixin, DeleteView):
  model = Pet
  success_url = '/owners/{owner_id}/'


# Sitter Views
class SitterCreate(LoginRequiredMixin, CreateView):
  model = Sitter

  fields = ['first_name', 'last_name', 'city', 'pet_experience', 'about']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class SitterUpdate(LoginRequiredMixin, UpdateView):
  model = Sitter
  fields = ['first_name', 'last_name', 'city', 'pet_experience', 'about']

class SitterDelete(LoginRequiredMixin, DeleteView):
  model = Sitter
  success_url = '/'

@login_required
def sitters_detail(request, sitter_id):
  my_key = os.environ['SECRET_KEY']
  sitter = Sitter.objects.get(id=sitter_id)
  return render(request, 'sitters/detail.html', {
    'sitter': sitter
  })

@login_required
def sitters_index(request):
  sitters = Sitter.objects.filter(user=request.user)
  return render(request, 'sitters/index.html', { 'sitters': sitters })


# photo views
# adds photos of pets to owners profile 
@login_required
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

# adds owner profile picture
@login_required
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

# adds siter profile picture
@login_required
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
            SitterProfile.objects.create(url=url, sitter_id=sitter_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('sitters_detail', sitter_id=sitter_id)

# sitter adds pictures to bottom
@login_required
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
            SitterPhoto.objects.create(url=url, sitter_id=sitter_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('sitters_detail', sitter_id=sitter_id)


# post views
@login_required
def posts_create(request, owner_id):
      owner = Owner.objects.get(id=owner_id)
      post_form = PostingForm()
      return render(request, 'owners/post_form.html', {
        'owner': owner,
        'post_form': post_form
      })

@login_required
def add_posting(request, owner_id):
  form = PostingForm(request.POST)
  if form.is_valid():
    new_posting = form.save(commit=False)
    new_posting.owner_id = owner_id
    new_posting.save()
  return redirect('index')

@login_required
def posts_index(request):
  posts = Post.objects.all() 
  return render(request, 'posts/index.html', { 
    'posts': posts,    
  })

@login_required
def posts_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  show_interest_form = ShowInterestForm()
  print(post.showinterest_set.all(), ' asdfgsfg')
  return render(request, 'posts/detail.html', {
    'post': post,
    'show_interest_form': show_interest_form,
  })

@login_required
def show_interest(request, post_id):
  form = ShowInterestForm(request.POST)
  if form.is_valid():
    sitter = Sitter.objects.get(user=request.user)
    show_interest = form.save(commit=False)
    show_interest.sitter_id = sitter.id
    show_interest.post_id = post_id
    show_interest.save()
  return redirect('posts_detail', post_id=post_id)

class PostUpdate(LoginRequiredMixin, UpdateView):
  model = Post
  fields = ['start_date', 'end_date', 'details']

class PostDelete(LoginRequiredMixin, DeleteView):
  model = Post
  success_url = '/posts/'
