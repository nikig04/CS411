from django.shortcuts import render, HttpResponse
import requests
import json
class Vividict(dict):
	def __missing__(self, key):
		value = self[key] = type(self)()
		return value
def index(request):
	# return HttpResponse('Hello World!')
	return render(request, 'FoodAPI/index.html')

def secondView(request):
	return HttpResponse('Testing. MIC Check 1 2.')



class FoodLists:
	cold = ["soup"]
	warm = ["salad"]

def recipes(request):
	weatherList = []
	userData = {}
	jsonList = []
	if request.POST:
		zipcode = request.POST.get('da_input')
		req = requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?zip=" + zipcode +",us&units=imperial&cnt=10&appid=e994992be112bc68c26ac350718dd773")
		jsonList.append(json.loads(req.content.decode("utf-8")))
		jsonList = jsonList[0]["list"]
		for data in jsonList:
			userData['date'] = data['dt']
			userData['forecast'] = data['weather'][0]['description']
			userData['max'] = data['temp']['max']
			userData['min'] = data['temp']['min']
			weatherList.append(userData)
			userData = {}
		weatherList = weatherList[1:]
	i = 1
	parsedData2 = []
	while i <(len(weatherList) + 1):
		max = weatherList[i-1]['max']
		if max > 44:
			foodList = FoodLists.warm
		elif max <= 44:
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

	return render(request, 'FoodAPI/recipes.html', {'data':parsedData2})

# def recipes(request):
# 	parsedData =[]
# 	if request.POST:
# 		ingredient = request.POST.get('da_input')
# 		jsonList = []
# 		req = requests.get('https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?ingredients=' + ingredient + '&limitLicense=false&number=5&ranking=1',
# 			headers={
# 		    "X-Mashape-Key": "Povx4QWmQlmshtcDOCYXxm8vjgMap1R7UvhjsnxZ2tUfwZjCmj",
# 		    "Accept": "application/json"
# 		  }
# 		)
# 		jsonList.append(json.loads(req.content))
# 		userData = {}
# 		jsonList = jsonList[0]
# 		for data in jsonList:
# 			userData['name_of_ingredient'] = data['title']
# 			userData['image_url'] = data['image']
# 			parsedData.append(userData)
# 			userData = {}
