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
	# to store confirm password
	# confirm_password = models.CharField(max_length=100)

	# returns name of user when object of user is printed
	def __str__(self):
		return self.username

class Weather(models.Model):

	zipcode = models.CharField(max_length=20)
	date = models.CharField(max_length=10)
	forecast = models.CharField(max_length=100)
	max_temp = models.CharField(max_length=5)
	min_temp = models.CharField(max_length=5)
	average_temp = models.CharField(max_length=5)

	# returns data and average temperature when object of weather is printed
	def __str__(self):
		# return '%s %s %s %s %s' % (self.date, self.forecast, self.max_temp, self.min_temp, self.average_temp)
		return '%s' % (self.average_temp)

class Recipe(models.Model):
	# foreign key connecting to weather table
	recipeWeather = models.ForeignKey(Weather, on_delete=models.CASCADE)
	# to store title
	title = models.CharField(max_length=100)
	# to store time to complete recipe
	readyInMinutes = models.IntegerField()
	# to store image
	image = models.CharField(max_length=100)
	# to store other stuff

	# returns title of recipe when object of recipes is printed
	def __str__(self):
		return self.title
