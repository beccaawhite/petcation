from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # path('posts/', views.paths, name='posts'),
    path('accounts/signup/', views.signup, name='signup'),
    path('owners/', views.owners_index, name='owners_index'),
    path('owners/<int:owner_id>/', views.owners_detail, name='detail'),
    path('owners/create/', views.OwnerCreate.as_view(), name='owners_create'),
    path('sitters/', views.sitters_index, name='sitters_index'),
    path('sitters/<int:sitter_id>/', views.sitters_detail, name='detail'),
    path('sitters/create/', views.SitterCreate.as_view(), name='sitters_create'),
]