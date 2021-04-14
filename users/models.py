from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100)
	last_name  = models.CharField(max_length=100)
	GENDER = (('M', 'Male'), ('F', 'Female'), ('O', 'Other'), )
	gender = models.CharField(max_length=50, choices=GENDER, default=None, null=True)
	location = models.CharField(max_length=50)
	bio = models.TextField()

	#default.jpg(default image of users without a picture) upload_to(folder where uploaded images are stored).
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

	def __str__(self):
		return f'{self.user.username} Profile' #formatted string to display username 

	#this save function resizes the image uploaded by the user to the user profile.
	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs) #run the save method of parent class(profile)

		img = Image.open(self.image.path)

		if img.height > 300 and img.width > 300: #checks the height and width of the image 
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

