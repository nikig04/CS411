from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from FoodAPI.forms import SignUpForm
# from FoodAPI.models import User
from FoodAPI.models import Weather

import random
import requests
import json
import datetime
from datetime import timedelta
from datetime import date, datetime
import sqlite3
import textwrap

class Vividict(dict):
	def __missing__(self, key):
		value = self[key] = type(self)()
		return value

class FoodLists:
	rain = ["stew", "buttermilk biscuit", "mac and cheese", "lasagna", "chili", "lentil soup", "grilled cheese",
			"chocolate chip cookie", "baked beans"]
	snow = ["mac and cheese", "roast chicken", "soup", "pasta", "hot chocolate", "pot pie", "muffin", "casserole"]
	cold = ["soup", "chili", "spaghetti", "pork chop", "stew", "mac and cheese", "lasagna", "chowder", "curry",
			"hot chocolate"]
	hot = ["salad", "shrimp", "chicken salad", "couscous", "sausage", "scallops", "hot dog", "burger", "corn"]
	summer = ["ice cream", "salad", "watermelon", "yogurt", "fig", "strawberry", "cucumber", "summer squash",
			  "gazpacho", "lemonade", "hot dog", "burger", "lobster", "summer"]
	winter = ["soup", "chili", "stew", "mac and cheese", "lasagna", "pot pie", "meatball", "quiche", "winter"]
	autumn = ["cobbler", "squash", "pumpkin", "crumble", "pear", "blackberry", "brussels sprouts", "leek", "autumn"]
	spring = ["apricot", "avocado", "asparagus", "strawberry", "salmon", "pea", "spring", "chicken", "snap pea"]


def index(request):
	return render(request, 'index.html')

@login_required
def home(request):
    return render(request, 'home.html')

# the function executes with the login url to take the inputs 
def signup(request):
    if request.method == 'POST':  # if the form has been filled
        form = SignUpForm(request.POST)
        if form.is_valid():  # All the data is valid
        	form.save()
        	username = form.cleaned_data.get('username')
        	raw_password = form.cleaned_data.get('password1')
        	user = authenticate(username=username, password=raw_password)
        	login(request, user)
        	return redirect('home')
           	# username = request.POST.get('username', '')
           	# email = request.POST.get('email', '')
           	# password = request.POST.get('password', '')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
    # return render(request, 'FoodAPI/signup.html', {'user_obj': user_obj,'is_registered':True }) # Redirect after POST

# #the function executes with the showdata url to display the list of registered users
# def showdata(request):
#    all_users = User.objects.all()
#    return render(request, 'registration/showdata.html', {'all_users': all_users, })

def recipes(request):
	weatherList = []
	userData = {}
	jsonList = []
	if request.POST:
		zipcode = request.POST.get('da_input')
		w_zipcode = Weather.objects.all().filter(zipcode=zipcode)

		if w_zipcode.exists():
			weatherList = Weather.objects.all().filter(zipcode=zipcode).values('average_temp')
			forecastList = Weather.objects.all().filter(zipcode=zipcode).values('forecast')

		else:
			req = requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?zip=" + zipcode +",us&units=imperial&cnt=10&appid=e994992be112bc68c26ac350718dd773")

			jsonList.append(json.loads(req.content.decode("utf-8")))
			# if 'city not found' in jsonList[0].values():
				# parsedData2 = [['','Please input a valid zipcode','','','','']]
				# return render(request, 'FoodAPI/recipes.html', {'data': parsedData2})
			jsonList = jsonList[0]["list"]
			# jsonList holds a list of dictionaries, each dictionary holding some weather info like date, description, temp max, temp min, etc
			for data in jsonList:
				# we're getting nine days worth of results so for each of the days, we're only storing the following pieces of info into userData and then into weatherList
				userData['date'] = data['dt']
				userData['forecast'] = data['weather'][0]['description']
				userData['max'] = data['temp']['max']
				userData['min'] = data['temp']['min']
				userData['average'] = round((userData['max'] + userData['min'])//2)
				
				# creating a weather object containing all the data
				weather_obj = Weather(zipcode=zipcode, date=userData['date'], 
					forecast=userData['forecast'], max_temp=userData['max'], 
					min_temp=userData['min'], average_temp=userData['average'])
				# saving all the data in the current object into the database
				weather_obj.save()

				# reset userData for next set
				userData = {}

			weatherList = Weather.objects.all().filter(zipcode=zipcode).values('average_temp')
			forecastList = Weather.objects.all().filter(zipcode=zipcode).values('forecast')

	i = 1
	parsedData2 = []	# once weatherList is filled, we iterate through it to get the average temp which is used to calculate types of food we want

	#This loop is for every day of the 10 days
	while i < (len(weatherList)):
		if i < 6:
			# Get the date of i days ahead of today
			current_date = date.today() + timedelta(days=(i))
			priority1 = False
			priority2 = False
			#foodList selector
			foodList = []
			average = weatherList[i]['average_temp']
			average = float(average)
			forecast = forecastList[i]['forecast']
			forecast = forecast.title()
			# forecast = forecast.encode('ascii', 'ignore')
			forecast = str(forecast)
			# Determine the season
			Y = 2000  # dummy leap year to allow input X-02-29 (leap day)
			seasons = [('winter', (date(Y, 1, 1), date(Y, 3, 20))),
					   ('spring', (date(Y, 3, 21), date(Y, 6, 20))),
					   ('summer', (date(Y, 6, 21), date(Y, 9, 22))),
					   ('autumn', (date(Y, 9, 23), date(Y, 12, 20))),
					   ('winter', (date(Y, 12, 21), date(Y, 12, 31)))]

			def get_season(now):
				if isinstance(now, datetime):
					now = now.date()
				now = now.replace(year=Y)
				return next(season for season, (start, end) in seasons
							if start <= now <= end)

			season = get_season(current_date)

			# Analyze the forecast, season, and temperature and decide what recipes to search
			if 'Drizzle' in forecast or 'Rain' in forecast:
				priority1 = True
				for ra in FoodLists.rain:
					foodList.append(ra)
			if 'Snow' in forecast:
				priority1 = True
				for sn in FoodLists.snow:
					foodList.append(sn)
			if average >= 73 and priority1 == False:
				priority2 = True
				for ho in FoodLists.hot:
					foodList.append(ho)
			if average <= 30 and priority1 == False:
				priority2 = True
				for co in FoodLists.cold:
					foodList.append(co)

			if season == 'winter' and priority2 == False and priority1 == False:
				for wi in FoodLists.winter:
					foodList.append(wi)

			if season == 'summer' and priority2 == False and priority1 == False:
				for su in FoodLists.summer:
					foodList.append(su)

			if season == 'spring' and priority2 == False and priority1 == False:
				for sp in FoodLists.spring:
					foodList.append(sp)

			if season == 'autumn' and priority2 == False and priority1 == False:
				for au in FoodLists.autumn:
					foodList.append(au)

			recipenum = 1
			for y in range(3):
				j = random.choice(foodList)
				foodList.remove(j)
				jsonList2 = []
				#userData2 = Vividict()
				req = requests.get(
					'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?limitLicense=false&number=1&tags=' + j,
					headers={
						"X-Mashape-Key": "Povx4QWmQlmshtcDOCYXxm8vjgMap1R7UvhjsnxZ2tUfwZjCmj",
						"Accept": "application/json"
					}
				)
				# unload the data from api call and append to jsonList
				jsonList2.append(json.loads(req.content.decode("utf-8")))


				for each_day in jsonList2:
					day_recipes = [current_date.strftime("%B %d, %Y") + " Recipe " + str(recipenum), average]
					day_recipes.append(forecast)
					k = 0
					#This loop says for each recipe in each day
					while k < len((each_day)['recipes']):
						#Add the recipe title
						day_recipes.append((each_day['recipes'][k]['title']))
						#Add the recipe URL
						day_recipes.append((each_day['recipes'][k]['spoonacularSourceUrl']))

						#Add the recipe ingredients
						z = 0
						ingredients = ""
						#for the list of ingredients for each recipe for each day
						while z < len(each_day['recipes'][k]['extendedIngredients']):
							#If the amount is something like 0.33333333333, we cut it off after 6 characters
							if len(str([each_day['recipes'][k]['extendedIngredients'][z]['amount']])) > 7:
								temp = str([each_day['recipes'][k]['extendedIngredients'][z]['amount']])
								temp = temp[0:7] + " "
								ingredients += temp
								
							#Otherwise, just add the amount
							else:
								ingredients += str([each_day['recipes'][k]['extendedIngredients'][z]['amount']])
							ingredients += str([each_day['recipes'][k]['extendedIngredients'][z]['unitLong']])
							ingredients += str([each_day['recipes'][k]['extendedIngredients'][z]['name']])
							ingredients += 'ENDTAG'
							z = z + 1
						#Parse the ingredients string and make the output pretty.
						ingredients = ingredients.replace('[','')
						ingredients = ingredients.replace(']', ' ')
						ingredients = ingredients.replace("u'", '')
						ingredients = ingredients.replace("'", "")
						ingredients = ingredients.replace(" ENDTAG", ", ")
					
						day_recipes.append(ingredients)

						k = k + 1
					recipenum += 1
				parsedData2.append(day_recipes)
			i = i + 1
		else:
			i = i + 1

	# returns recipes to html
	# print(parsedData2)
	return render(request, 'FoodAPI/recipes.html', {'data':parsedData2})

