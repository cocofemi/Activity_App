from django.db.models.signals import post_save #fired after an object as been saved
from django.contrib.auth.models import User #imports user model (sends the signal)
from django.dispatch import receiver #recieves the sent signal from user
from .models import Profile

"""
@receiver(a decorator that receives a signal from the sender). 

The function below automatically creates a profile object for a new user

It takes a receiver signal with the sender being the User.
"""
@receiver(post_save, sender=User) 
def create_profile(sender, instance, created, **kwargs): 
	if created:
		Profile.objects.create(user=instance) # it creates a new User Profile for the user if the user was created. 

"""
The function below saves the profile object every time the user profile is created.

 kwargs accepts any keyword arguments unto the end of the function
"""
@receiver(post_save, sender=User) 
def save_profile(sender, instance, **kwargs):
	instance.profile.save()

#kwargs accepts any additional arguments