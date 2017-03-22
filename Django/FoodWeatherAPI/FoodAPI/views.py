from django.shortcuts import render, HttpResponse
import requests
import json
def index(request):
	return HttpResponse('Hello World!')
def secondView(request):
	return HttpResponse('My second view!')
def profile(request):
	parsedData =[]
	if request.POST:
		ingredient = request.POST.get('da_input')
		jsonList = []
		req = requests.get('https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?ingredients=' + ingredient + '&limitLicense=false&number=5&ranking=1',
			headers={
		    "X-Mashape-Key": "Povx4QWmQlmshtcDOCYXxm8vjgMap1R7UvhjsnxZ2tUfwZjCmj",
		    "Accept": "application/json"
		  }
		)
		jsonList.append(json.loads(req.content))
		userData = {}
		jsonList = jsonList[0]
		for data in jsonList:
			userData['name_of_ingredient'] = data['title']
			userData['image_url'] = data['image']
		parsedData.append(userData)
		# print (parsedData)
		# print(jsonList[0])
	return render(request, 'FoodAPI/profile.html', {'data':parsedData})