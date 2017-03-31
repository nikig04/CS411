import requests
import json
class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

class FoodLists:
    cold = ["soup"]
    warm = ["salad"]

def weather(zip):
    weatherList = []
    userData = {}
    jsonList = []
    req = requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?zip=" + zip +",us&units=imperial&cnt=10&appid=e994992be112bc68c26ac350718dd773")
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
    food(weatherList)

def food(weatherList):
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



    print(parsedData2)
    return parsedData2

weather("02467")
