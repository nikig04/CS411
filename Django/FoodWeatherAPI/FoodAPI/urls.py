from django.conf.urls import url
from . import views

app_name = 'FoodAPI'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^showdata/$', views.showdata, name='showdata'),
	url(r'^recipes/$', views.recipes, name='recipes'),
	# url(r'^recommendation/$', views.recipes, name='recommendation'),

	]
