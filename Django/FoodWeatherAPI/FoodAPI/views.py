from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from FoodAPI.forms import SignUpForm
from FoodAPI.models import Weather
from FoodAPI.models import Profile

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

class FoodLists: #Lists of food that we use for our recipe search, based on research online.
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
	not_vegan = ["buttermilk biscuit", "mac and cheese", "grilled cheese", "roast chicken", "pork chop",
				 "shrimp", "chicken salad", "sausage", "scallops", "hot dog", "meatball", "salmon", "chicken", "lobster"]
	not_vegetarian = ["roast chicken", "pork chop", "shrimp", "chicken salad", "sausage", "scallops", "hot dog", "meatball",
					  "salmon", "chicken"]
	not_dairy_free = ["buttermilk biscuit", "mac and cheese", "grilled cheese"]


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
        	user = form.save()
        	user.refresh_from_db() # load the profile instance created by the signal
        	user.profile.vegetarian = form.cleaned_data.get('vegetarian')
        	user.profile.vegan = form.cleaned_data.get('vegan')
        	user.profile.gluten_free = form.cleaned_data.get('gluten_free')
        	user.profile.dairy_free = form.cleaned_data.get('dairy_free')
        	user.save()
        	raw_password = form.cleaned_data.get('password1')
        	user = authenticate(username=user.username, password=raw_password)
        	login(request, user)
        	return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


#the function executes with the showdata url to display the list of registered users
def showdata(request):
   all_users = User.objects.all()
   return render(request, 'registration/showdata.html', {'all_users': all_users, })

def recipes(request):
	weatherList = []
	userData = {}
	jsonList = []
	if request.POST:

		current_user = request.user.id
		vegetarian = Profile.objects.all().filter(user_id=current_user).values('vegetarian') #Get their dietary restrictions
		vegan = Profile.objects.all().filter(user_id=current_user).values('vegan')
		gluten_free = Profile.objects.all().filter(user_id=current_user).values('gluten_free')
		dairy_free = Profile.objects.all().filter(user_id=current_user).values('dairy_free')

		vegetarian= vegetarian[0]['vegetarian']
		vegan = vegan[0]['vegan']
		gluten_free = gluten_free[0]['gluten_free']
		dairy_free = dairy_free[0]['dairy_free']

		zipcode = request.POST.get('da_input')  #here, we get the users input and assign it as our zipcode
		if zipcode == "":
			parsedData2 = [['', 'Please input a valid zipcode', '', '', '', '']] # if the zipcode is empty, tell them to input a zip code
			return render(request, 'FoodAPI/recipes.html', {'data': parsedData2})


		w_zipcode = Weather.objects.all().filter(zipcode=zipcode)
		if w_zipcode.exists(): #If the zipcode is in the database, just get the forecast and average_temp
			weatherList = Weather.objects.all().filter(zipcode=zipcode).values('average_temp')
			forecastList = Weather.objects.all().filter(zipcode=zipcode).values('forecast')

		else: #If its not in the database, we have to add it
			req = requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?zip=" + zipcode +",us&units=imperial&cnt=10&appid=e994992be112bc68c26ac350718dd773") #hit the api to get the zip code weather info

			jsonList.append(json.loads(req.content.decode("utf-8")))
			if 'city not found' in jsonList[0].values():
				parsedData2 = [['','Please input a valid zipcode','','','','']] #If the api doesn't recognize the zip code, it must be invalid, so tell them to put in a valid zipcode.
				return render(request, 'FoodAPI/recipes.html', {'data': parsedData2})
			jsonList = jsonList[0]["list"]

			# jsonList holds a list of dictionaries, each dictionary holding some weather info like date, description, temp max, temp min, etc
			for data in jsonList:
				# we're getting five days worth of results so for each of the days, we're only storing the following pieces of info into userData and then into weatherList
				userData['date'] = data['dt']
				userData['forecast'] = data['weather'][0]['description']
				userData['max'] = data['temp']['max']
				userData['min'] = data['temp']['min']
				userData['average'] = round((userData['max'] + userData['min'])//2) #we use max and min to calculate the average temperature throughout the day
				
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

	#This loop is for every day of the 5 days
	while i < (len(weatherList)):

		if i < 6:
			# Get the date of i days ahead of today
			current_date = date.today() + timedelta(days=(i))
			priority1 = False #Used in determine what recipes to search below
			priority2 = False

			# foodList selector
			foodList = []
			average = weatherList[i]['average_temp']
			average = float(average) #It comes out as a byte object, so convert to float so we can compare below
			forecast = forecastList[i]['forecast']
			forecast = forecast.title()
			forecast = str(forecast) #Convert so str

			# Table used to determine the season
			Y = 2000  # dummy leap year to allow input X-02-29 (leap day)
			seasons = [('winter', (date(Y, 1, 1), date(Y, 3, 20))),
					   ('spring', (date(Y, 3, 21), date(Y, 6, 20))),
					   ('summer', (date(Y, 6, 21), date(Y, 9, 22))),
					   ('autumn', (date(Y, 9, 23), date(Y, 12, 20))),
					   ('winter', (date(Y, 12, 21), date(Y, 12, 31)))]

			def get_season(now): #Determine the season
				if isinstance(now, datetime):
					now = now.date()
				now = now.replace(year=Y)
				return next(season for season, (start, end) in seasons
							if start <= now <= end)

			season = get_season(current_date) #Based on the current date, find out what season it is.

			# Analyze the forecast, season, and temperature and decide what recipes to search
			if 'Drizzle' in forecast or 'Rain' in forecast: #If the forecast is rainy or snowy, we consider that highest priority and will search for recipes based on that forecast
				priority1 = True
				for ra in FoodLists.rain:
					foodList.append(ra)
			if 'Snow' in forecast:
				priority1 = True
				for sn in FoodLists.snow:
					foodList.append(sn)
			if average >= 73 and priority1 == False:  #If the forecast was not rainy or snowy, then we look at the average temperature and decide if we should pick recipes if it is hot or cold
				priority2 = True
				for ho in FoodLists.hot:
					foodList.append(ho)
			if average <= 30 and priority1 == False:
				priority2 = True
				for co in FoodLists.cold:
					foodList.append(co)

			if season == 'winter' and priority2 == False and priority1 == False: #If it is neither hot nor cold and neither rainy or snowy, we will simply check what season it is and return recipes with food from that season
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
			for y in range(3): #we want 3 recipes for each day, so this loop begins each recipe for this day
				if vegan:  												#before we pick a food from the list, we must remove any foods in the list that don't comply with this users dietary restrictions
					for item in FoodLists.not_vegan: 					#these next few lines use our premade lists that identify any food that are either
						while item in foodList: foodList.remove(item) 	#not vegan, not vegetarian, or not dairy free, and remove them from the food list
				if vegetarian:											#if the user has any of these dietary restrictions
					for item in FoodLists.not_vegetarian:
						while item in foodList: foodList.remove(item)
				if dairy_free:
					for item in FoodLists.not_dairy_free:
						while item in foodList: foodList.remove(item)
				tags = random.choice(foodList)							#now that we have a proper foodList for this user, pick a random food
				foodList.remove(tags)									#remove that ingredient from the foodList, because we don't want to recommend
				if vegan:												#Multiple recipes on the same day with the same ingredient
					tags += "%2C+vegan"
				if vegetarian:
					tags += "%2C+vegetarian"							#Now, add the proper tag to the api tags based on their restrictions
				if gluten_free:
					tags += "%2C+gluten+free"
				if dairy_free:
					tags += "%2C+dairy+free"
				jsonList2 = []
				req = requests.get(
					'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?limitLicense=false&number=1&tags=' + tags,  #finally, request a random recipe from the API with the tags we've given
					headers={
						"X-Mashape-Key": "Povx4QWmQlmshtcDOCYXxm8vjgMap1R7UvhjsnxZ2tUfwZjCmj",
						"Accept": "application/json"
					}
				)
				# unload the data from api call and append to jsonList
				jsonList2.append(json.loads(req.content.decode("utf-8")))


				for each_day in jsonList2: #jsonList2 will contain one recipe for one day
					day_recipes = [current_date.strftime("%B %d, %Y") + " Recipe " + str(recipenum), average]
					day_recipes.append(forecast)
					k = 0
					#This loop says for each recipe in each day. As of now, we just get one recipe for one day at a time
					while k < len((each_day)['recipes']):
						#Add the recipe title
						day_recipes.append((each_day['recipes'][k]['title']))
						#Add the recipe URL
						day_recipes.append((each_day['recipes'][k]['spoonacularSourceUrl']))

						#Add the recipe ingredients. We need to do some parsing...
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
						#Now, we can add the ingredients for this recipe
						day_recipes.append(ingredients)

						k = k + 1
					recipenum += 1
				#Now, we add the title, url and ingredients to our final list (ParsedData2) and then we move on to the next recipe or next day.
				parsedData2.append(day_recipes)
			i = i + 1
		else:
			i = i + 1
			
	return render(request, 'FoodAPI/recipes.html', {'data':parsedData2})

