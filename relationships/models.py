from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

class Relationship(models.Model):
	from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
	to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_set')
	date_added = models.DateTimeField(default=datetime.now)


	def __str__(self):
		return "%s is following %s" % (self.from_user.username, self.to_user.username)

	def save(self, **kwargs):
		"""
		A mostly-generic save method, except that it validates that the user
		is not attempting to follow themselves.
		"""
		if self.from_user == self.to_user:
			raise ValueError("Cannot follow yourself.")
		super(Relationship, self).save(**kwargs)

	class Meta:
		unique_together = (('to_user', 'from_user'),)
