from django.shortcuts import render, HttpResponse
from FoodAPI.forms import UserForm
from FoodAPI.models import User
from FoodAPI.models import Weather

import requests
import json
import sqlite3
# import forms

class Vividict(dict):
	def __missing__(self, key):
		value = self[key] = type(self)()
		return value

class FoodLists:
	cold = ["soup"]
	warm = ["salad"]

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
			# weatherList = list(w_zipcode.values())
			weatherList = Weather.objects.all().filter(zipcode=zipcode).values('average_temp')
			print ('exists:', weatherList)

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
					min_temp=userData['min'], average_temp=userData['average_temp'])
				# saving all the data in the current object into the database
				weather_obj.save()

				# reset userData for next set
				userData = {}

			weatherList = Weather.objects.all().filter(zipcode=zipcode).values('average_temp')
			print ('new:', weatherList)
				
	i = 1
	parsedData2 = []
	# once weatherList is filled, we iterate through it to get the average temp which is used to calculate types of food we want
	while i < (len(weatherList) + 1):
		average = weatherList[i-1]['average_temp']
		if average > 44:
			foodList = FoodLists.warm
		elif average <= 44:
			foodList = FoodLists.cold
		# for now foodList is only one thing but later it could be more.
		# from that foodList, we're accessing the food api to get ingredients (for now it's soup or salad)
		for j in foodList:
			jsonList2 = []
			userData2 = Vividict()
			req = requests.get(
				'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?query=' + j + '&number=3',
				headers={
					"X-Mashape-Key": "Povx4QWmQlmshtcDOCYXxm8vjgMap1R7UvhjsnxZ2tUfwZjCmj",
					"Accept": "application/json"
				}
			)
			# unload the data from api call and append to jsonList
			jsonList2.append(json.loads(req.content.decode("utf-8")))

			# for each of the recipes (3 for each day) we're adding it to userData2

			for data in jsonList2:
				k = 0
				day_recipes=["Day "+str(i), average]

				while k < len((data)['results']):
					userData2["Day_" +str(i) + "_recipes"]["Recipe_" + str(k)] = (data['results'][k]['title'])
					day_recipes.append((data['results'][k]['title']))
					k = k + 1
			# we're apeending stuff from userData2 into one list called parsedData2
			#parsedData2.append(userData2)
			parsedData2.append(day_recipes)
			# print(parsedData2)
			userData2 = Vividict()

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