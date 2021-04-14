from django.contrib import admin
from .models import Profile

# Register your models here.

#registers a new model to display in the localHost:8000/admin 
admin.site.register(Profile)
