import requests
import json
class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

class FoodLists:
    cold = ["soup"]
    warm = ["salad"]

def recipes(request):
    weatherList = []
    userData = {}
    jsonList = []
    w = Weather.objects.all().filter(zipcode=zipcode)
    # w = Weather.objects.prefetch_related(zipcode).all()\
    #                  .order_by('date')

    if w.exists():
        print (w)
    else:
        req = requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?zip=" + zipcode +",us&units=imperial&cnt=10&appid=e994992be112bc68c26ac350718dd773")
        jsonList.append(json.loads(req.content.decode("utf-8")))
        jsonList = jsonList[0]["list"]
        for data in jsonList:
            userData['date'] = data['dt']
            userData['forecast'] = data['weather'][0]['description']
            userData['max'] = data['temp']['max']
            userData['min'] = data['temp']['min']
            userData['average'] = (userData['max'] + userData['min'])/2
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
    while i <(len(weatherList) + 1):
        average = weatherList[i-1]['average']
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

    # return render(request, 'FoodAPI/recipes.html', {'data':parsedData2})

# def recipes(zip):
#     weatherList = []
#     userData = {}
#     jsonList = []
#     req = requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?zip=" + zip +",us&units=imperial&cnt=10&appid=e994992be112bc68c26ac350718dd773")
#     jsonList.append(json.loads(req.content.decode("utf-8")))
#     jsonList = jsonList[0]["list"]
#     for data in jsonList:
#         userData['date'] = data['dt']
#         userData['forecast'] = data['weather'][0]['description']
#         userData['max'] = data['temp']['max']
#         userData['min'] = data['temp']['min']
#         userData['average'] = (userData['max'] + userData['min'])/2
#         weatherList.append(userData)
#         userData = {}
#     weatherList = weatherList[1:]
#     # print (weatherList)

#     i = 1
#     parsedData2 = []
#     while i <(len(weatherList) + 1):

#         max = weatherList[i-1]['max']
#         if max > 44:
#             foodList = FoodLists.warm
#         elif max <= 44:
#             foodList = FoodLists.cold


#         for j in foodList:
#             jsonList2 = []
#             userData2 = Vividict()
#             req = requests.get(
#                 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?query=' +j + '&number=3',
#                 headers={
#                     "X-Mashape-Key": "Povx4QWmQlmshtcDOCYXxm8vjgMap1R7UvhjsnxZ2tUfwZjCmj",
#                     "Accept": "application/json"
#                 }
#                 )
#             jsonList2.append(json.loads(req.content.decode("utf-8")))
#             for data in jsonList2:
#                 k = 0
#                 while k < len((data)['results']):

#                     userData2["Day_" + str(i) + " recipes"]["Recipe_" + str(k)] = (data['results'][k]['title'])
#                     k = k + 1


#             parsedData2.append(userData2)
#             userData2 = Vividict()
#         i = i + 1


#     print(parsedData2)
#     return parsedData2
#     # print(jsonList2)
#     # return jsonList2

recipes("02116")
