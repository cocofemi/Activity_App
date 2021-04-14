from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# from django_extensions.db.fields import AutoSlugField 
# Create your models here.

class Activity(models.Model):
	author 			= models.ForeignKey(User, on_delete=models.CASCADE)
	name 			= models.CharField(max_length=250)
	slug 			= models.SlugField(null=True, max_length=50)
	# slug = AutoSlugField(_('slug'), max_length=50, unique=True, populate_from=('name'), null=True)
	description 	= models.TextField()
	# target 			= models.TextField(max_length=150)
	image			= models.ImageField(null=True, upload_to='activity_pics', blank=True)
	category_chocies = (('Arts', 'Arts'), ('Adventure', 'Adventure'), 
		('Business', 'Business'), ('Design', 'Design'), ('Entertainment', 'Entertainment'), ('Education', 'Education'), 
		('Health', 'Health'), ('Fitness', 'Fitness'), 
		('Fashion', 'Fashion'), ('Food', 'Food'), ('Music', 'Music'), ('Programming', 'Programming'), ('Startup', 'Startup'),
		('Technology', 'Technology'), ('Other', 'Other'), )
	category		= models.CharField(max_length=100, default=None, choices=category_chocies, null=True)
	bookmark		= models.ManyToManyField(User, related_name='bookmark', blank=True)
	start_date 		= models.DateTimeField(default=timezone.now)
	end_date		= models.DateTimeField(default=timezone.now)
	date_posted	 	= models.DateTimeField(default=timezone.now) #set to the actual time the post was updated

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('activity:activity-list', kwargs={'username': self.author })

	# def save(self, *args, **kwargs):
	# 	super(Activity, self).save(*args, **kwargs) #run the save method of parent class(profile)

	# 	img = Image.open(self.image.path)

	# 	if img.height > 300 and img.width > 300: #checks the height and width of the image 
	# 		output_size = (300, 300)
	# 		img.thumbnail(output_size)
	# 		img.save(self.image.path)
