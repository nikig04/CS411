from django.shortcuts import render, HttpResponse
from FoodAPI.forms import UserForm
from FoodAPI.models import User
from FoodAPI.models import Weather

import requests
import json
import sqlite3
import forms

class Vividict(dict):
	def __missing__(self, key):
		value = self[key] = type(self)()
		return value

class FoodLists:
	cold = ["soup"]
	warm = ["salad"]

# class CreateContactView(CreateView):
#     model = Contact
#     template_name = 'edit_contact.html'
#     form_class = forms.ContactForm

# class UpdateContactView(UpdateView):

#     model = Contact
#     template_name = 'edit_contact.html'
#     form_class = forms.ContactForm
    
def index(request):
	# return HttpResponse('Hello World!')
	return render(request, 'FoodAPI/index.html')

#the function executes with the signup url to take the inputs 
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

# CODE TO DISPLAY IN HTML
# {% for record in result %}
#     {{record.c}}, {{record.e}}, 
#     {% for animal in record.animal_set|slice:":1" %}
#         {{animal.p}}
#     {% endfor %}
# {% endfor %}

def recipes(request):
	weatherList = []
	userData = {}
	jsonList = []
	if request.POST:
		zipcode = request.POST.get('da_input')
		w = Weather.objects.all().filter(zipcode=zipcode).values('average_temp')

		if w.exists():
			weatherList = w
			# print (weatherList)
		else:
			req = requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?zip=" + zipcode +",us&units=imperial&cnt=10&appid=e994992be112bc68c26ac350718dd773")
			jsonList.append(json.loads(req.content.decode("utf-8")))
			jsonList = jsonList[0]["list"]
			for data in jsonList:
				userData['date'] = data['dt']
				userData['forecast'] = data['weather'][0]['description']
				userData['max'] = data['temp']['max']
				userData['min'] = data['temp']['min']
				userData['average'] = round((userData['max'] + userData['min'])//2)
				weatherList.append(userData)
				
				# creating a weather object containing all the data
				weather_obj = Weather(zipcode=zipcode, date=userData['date'], 
					forecast=userData['forecast'], max_temp=userData['max'], 
					min_temp=userData['min'], average_temp=userData['average'])
				# saving all the data in the current object into the database
				weather_obj.save()
				# reset userData for next set
				userData = {}
			weatherList = weatherList[1:]
	
	i = 1
	parsedData2 = []
	while i < (len(weatherList) + 1):
		average = weatherList[i-1]['average_temp']
		# print(average)
		if average > 44:
			foodList = FoodLists.warm
		elif average <= 44:
			foodList = FoodLists.cold
		for j in foodList:
			jsonList2 = []
			userData2 = Vividict()
			req = requests.get(
				'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?query=' +j + '&number=3',
				headers={
					"X-Mashape-Key": "Povx4QWmQlmshtcDOCYXxm8vjgMap1R7UvhjsnxZ2tUfwZjCmj",
					"Accept": "application/json"
				}
			)
			jsonList2.append(json.loads(req.content.decode("utf-8")))
			for data in jsonList2:
				k = 0
				while k < len((data)['results']):
					userData2["Day_" +str(i) + " recipes"]["Recipe_" + str(k)] = (data['results'][k]['title'])
					k = k + 1

			parsedData2.append(userData2)
			userData2 = Vividict()

		i = i + 1

	# return render(request, 'FoodAPI/recipes.html', {'data':weatherList})

	return render(request, 'FoodAPI/recipes.html', {'data':parsedData2})











# PREVIOUS
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