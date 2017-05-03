from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

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

class Profile(models.Model):
	# to store username
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	# # to store location
	# location = models.CharField(max_length=30, blank=True)
	# to store if vegetarian
	vegetarian = models.BooleanField(default=False)
	# to store if vegan
	vegan = models.BooleanField(default=False)
	# to store if gluten_free
	gluten_free = models.BooleanField(default=False)
	# to store if dairy_free
	dairy_free = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    

# class Recipe(models.Model):
# 	# foreign key connecting to weather table
# 	recipeWeather = models.ForeignKey(Weather, on_delete=models.CASCADE)
# 	# to store title
# 	title = models.CharField(max_length=100)
# 	# to store time to complete recipe
# 	readyInMinutes = models.IntegerField()
# 	# to store image
# 	image = models.CharField(max_length=100)
# 	# to store other stuff

# 	# returns title of recipe when object of recipes is printed
# 	def __str__(self):
# 		return self.title
