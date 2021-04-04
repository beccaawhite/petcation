from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Owner, Sitter, Pet, Post


admin.site.register(Owner)
admin.site.register(Sitter)
admin.site.register(Pet)
admin.site.register(Post)