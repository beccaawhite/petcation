from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # path('posts/', views.paths, name='posts'),
    path('accounts/signup/', views.signup, name='signup'),
    # path('owners/', views.owners_index, name='owners_index'),
    path('owners/<int:owner_id>/', views.owners_detail, name='owners_detail'),
    path('owners/create/', views.OwnerCreate.as_view(), name='owners_create'),
    path('owners/<int:pk>/update/', views.OwnerUpdate.as_view(), name='owners_update'),
    path('owners/<int:pk>/delete/', views.OwnerDelete.as_view(), name='owners_delete'),
    path('owners/<int:owner_id>/pet_create/', views.pets_create, name='pets_create'),
    path('owners/<int:owner_id>/add_pet/', views.add_pet, name='add_pet'),    
    path('owners/<int:owner_id>/post_create/', views.posts_create, name='posts_create'),
    path('owners/<int:owner_id>/add_posting/', views.add_posting, name='add_posting'),
    path('pets/<int:pet_id>/', views.pets_detail, name='pets_detail'),
    path('pets/<int:pk>/update/', views.PetUpdate.as_view(), name='pets_update'),    
    path('pets/<int:pk>/delete/', views.PetDelete.as_view(), name='pets_delete'),
    # path('sitters/', views.sitters_index, name='sitters_index'),
    path('sitters/<int:sitter_id>/', views.sitters_detail, name='sitters_detail'),
    path('sitters/create/', views.SitterCreate.as_view(), name='sitters_create'),
    path('sitters/<int:pk>/update/', views.SitterUpdate.as_view(), name='sitters_update'),
    path('sitters/<int:pk>/delete/', views.SitterDelete.as_view(), name='sitters_delete'),
    path('sitters/<int:sitter_id>/add_photo/', views.add_photo, name='add_photo'),
    path('posts/', views.posts_index, name='index'),
    path('posts/<int:post_id>/show_interest/', views.show_interest, name='show_interest'),
]
 

