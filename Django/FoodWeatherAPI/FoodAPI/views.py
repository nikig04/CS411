from django.shortcuts import render, HttpResponse
from FoodAPI.forms import UserForm
from FoodAPI.models import User
from FoodAPI.models import Weather
import random
import requests
import json
import sqlite3
# import forms

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

# DON't NEED TO TOUCH THIS
# class CreateContactView(CreateView):
#     model = Contact
#     template_name = 'edit_contact.html'
#     form_class = forms.ContactForm

# class UpdateContactView(UpdateView):

#     model = Contact
#     template_name = 'edit_contact.html'
#     form_class = forms.ContactForm
    
def index(request):
	return render(request, 'FoodAPI/index.html')

# the function executes with the signup url to take the inputs 
def signup(request):
   if request.method == 'POST':  # if the form has been filled

       form = UserForm(request.POST)

       if form.is_valid():  # All the data is valid
           username = request.POST.get('username', '')
           email = request.POST.get('email', '')
           password = request.POST.get('password', '')
       # creating an user object containing all the data
       user_obj = User(username=username, email=email, password=password)
       # saving all the data in the current object into the database
       user_obj.save()

       return render(request, 'FoodAPI/signup.html', {'user_obj': user_obj,'is_registered':True }) # Redirect after POST

   else:
       form = UserForm()  # an unboundform

       return render(request, 'FoodAPI/signup.html', {'form': form})

#the function executes with the showdata url to display the list of registered users
def showdata(request):
   all_users = User.objects.all()
   return render(request, 'FoodAPI/showdata.html', {'all_users': all_users, })


def recipes(request):
	weatherList = []
	userData = {}
	jsonList = []
	if request.POST:
		zipcode = request.POST.get('da_input')
		w_zipcode = Weather.objects.all().filter(zipcode=zipcode)

		if w_zipcode.exists():
			weatherList = Weather.objects.all().filter(zipcode=zipcode).values('average_temp')

		else:
			req = requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?zip=" + zipcode +",us&units=imperial&cnt=10&appid=e994992be112bc68c26ac350718dd773")
			jsonList.append(json.loads(req.content.decode("utf-8")))
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

	i = 1
	parsedData2 = []
	# once weatherList is filled, we iterate through it to get the average temp which is used to calculate types of food we want

	#This loop is for every day of the 10 days
	while i < (len(weatherList) + 1):
		if i < 6:
			#foodList selector
			foodList = []
			average = weatherList[i-1]['average_temp']
			if average > 50:
				for ii in FoodLists.hot:
					foodList.append(ii)
			elif average <= 50:
				for ii in FoodLists.cold:
					foodList.append(ii)





			# for now foodList is only one thing but later it could be more.
			# from that foodList, we're accessing the food api to get ingredients (for now it's soup or salad)


			recipenum = 1
			for y in range(3):
				j = random.choice(foodList)
				foodList.remove(j)
				print(j)
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
					day_recipes = ["Day " + str(i) + " Recipe " + str(recipenum), average]
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



	print(parsedData2)

	# returns recipes to html
	# print(parsedData2)
	return render(request, 'FoodAPI/recipes.html', {'data':parsedData2})




# BACKUP
# def recipes(request):
# 	weatherList = []
# 	userData = {}
# 	jsonList = []
# 	if request.POST:
# 		zipcode = request.POST.get('da_input')
# 		req = requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?zip=" + zipcode +",us&units=imperial&cnt=10&appid=e994992be112bc68c26ac350718dd773")
# 		jsonList.append(json.loads(req.content.decode("utf-8")))
# 		jsonList = jsonList[0]["list"]
# 		for data in jsonList:
# 			userData['date'] = data['dt']
# 			userData['forecast'] = data['weather'][0]['description']
# 			userData['max'] = data['temp']['max']
# 			userData['min'] = data['temp']['min']
# 			weatherList.append(userData)
# 			userData = {}

# 		weatherList = weatherList[1:]

# 	i = 1
# 	parsedData2 = []
# 	while i <(len(weatherList) + 1):
# 		max = weatherList[i-1]['max']
# 		if max > 44:
# 			foodList = FoodLists.warm
# 		elif max <= 44:
# 			foodList = FoodLists.cold
# 		for j in foodList:
# 			jsonList2 = []
# 			userData2 = Vividict()
# 			req = requests.get(
# 				'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?query=' +j + '&number=3',
# 				headers={
# 					"X-Mashape-Key": "Povx4QWmQlmshtcDOCYXxm8vjgMap1R7UvhjsnxZ2tUfwZjCmj",
# 					"Accept": "application/json"
# 				}
# 			)
# 			jsonList2.append(json.loads(req.content.decode("utf-8")))
# 			for data in jsonList2:
# 				k = 0
# 				while k < len((data)['results']):
# 					userData2["Day_" +str(i) + " recipes"]["Recipe_" + str(k)] = (data['results'][k]['title'])
# 					k = k + 1


# 			parsedData2.append(userData2)
# 			userData2 = Vividict()

# 		i = i + 1

# 	return render(request, 'FoodAPI/recipes.html', {'data':parsedData2})