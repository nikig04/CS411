# Feather
Website for Seasonal food choices personalized to you!

Feather is a web application that allows users to view the weather for the week and plan their meals accordingly for the comfort of their lives. Feather uses an open weather API and a food API to calculate and return simple meals for the right weather.

You may find further information about Feather in the "Documentation" folder of this repository.

Packages to install are included in Documentation under the name, 'requirements.txt'

Note: 
As this app has yet to be live, everything is run under localhost using a virtual environment with Python and Django framework. Once you have the env set up, simply go to Django/FoodWeatherAPI and enter: python manage.py runserver, then go to http://localhost:8000/ and the site will be up!

Also, we had setup a cronjob that would clear the weather data in the database daily, because we dont want to cache old weather data. It doesn't run automatically (because the app is not live), but it can be activated by running:
python manage.py runcrons.
If we were to go live, we would set it up to run at 00:00 every day so that we don't have old weather data.




