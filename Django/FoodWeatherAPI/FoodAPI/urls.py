from django.conf.urls import url, include
from django.contrib.auth import views as auth_views # <--
from . import views

app_name = 'FoodAPI'

urlpatterns = [
	url(r'^recipes/$', views.recipes, name='recipes'),

	]
