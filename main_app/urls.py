from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # path('posts/', views.paths, name='posts'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/signup/owner', views.owners_signup, name='owners_signup'),
    path('accounts/signup/sitter', views.sitters_signup, name='sitters_signup'),
]