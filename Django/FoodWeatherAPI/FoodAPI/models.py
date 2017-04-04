from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
	# to store username
	username = models.CharField(max_length=100)
	# to store email
	email = models.CharField(max_length=100)
	# to store password
	password = models.CharField(max_length=100)

	# returns name of user when object of user is printed
	def __str__(self):
		return self.username


