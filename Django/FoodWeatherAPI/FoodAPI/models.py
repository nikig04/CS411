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

class Weather(models.Model):

	zipcode = models.CharField(max_length=20)
	date = models.CharField(max_length=20)
	forecast = models.CharField(max_length=100)
	max_temp = models.FloatField()
	min_temp = models.FloatField()
	average_temp = models.FloatField()

	# returns zipcode when object of weather is printed
	def __str__(self):
		return self.zipcode

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
