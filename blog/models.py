from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from activity.models import Activity
from PIL import Image
# from django_extensions.db.fields import AutoSlugField 
# Create your models here.

class Post(models.Model):
	activity 	= models.ForeignKey(Activity, on_delete=models.CASCADE) #CASCADE means if the activity is deleted the posts under it too are deleted.
	# slug 		= models.SlugField(max_length=50, unique=True, null=True)
	content 	= models.TextField()
	image		= models.ImageField(null=True, upload_to='post_pics')
	favorite	= models.ManyToManyField(User, related_name='favorite', blank=True)
	likes		= models.ManyToManyField(User, related_name='likes', blank=True)
	date_posted = models.DateTimeField(default=timezone.now) #set to the actual time the post was updated
	author 		= models.ForeignKey(User, on_delete=models.CASCADE) #a foreign key(one to many relationship with the User model) 

	# def save(self, *args, **kwargs):
	# 	super(Post, self).save(*args, **kwargs) #run the save method of parent class(profile)
	# 	img = Image.open(self.image.path)

	# 	if img.height > 300 and img.width > 300: #checks the height and width of the image 
	# 		output_size = (500, 500)
	# 		img.thumbnail(output_size)
	# 		img.save(self.image.path)

	#function to return the title of the post as a string
	def __str__(self):
		return self.content[:80]

	def total_likes(self):
		return self.likes.count()

	def get_absolute_url(self):
		""" this method uses the reverse function which returns the url as a string rather than redirecting to a new page
		it takes kwargs with the users pk(users id) this function works for when PostCreateView is called to create a new post. On saving the url is reversed to the post detail page.
		"""
		return reverse('post:user-posts', kwargs={'username': self.author})

