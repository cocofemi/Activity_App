from django.db import models
from django.utils import timezone
from blog.models import Post
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Comment(models.Model):
	author 		= models.ForeignKey(User, on_delete=models.CASCADE)
	post 		= models.ForeignKey(Post, on_delete=models.CASCADE)
	content 	= models.TextField()
	# slug 		= models.SlugField(max_length=50, unique=True, null=True)
	image		= models.ImageField(null=True, upload_to='post_pics', blank=True)
	likes		= models.ManyToManyField(User, related_name='comment_likes', blank=True)
	date_posted = models.DateTimeField(default=timezone.now)
	parent 		= models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')


	def __str__(self):
		return self.content[:80]

	def get_absolute_url(self):
		return reverse('post:user-posts', kwargs={'username': self.author})