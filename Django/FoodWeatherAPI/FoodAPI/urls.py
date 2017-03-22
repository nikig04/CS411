from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^test/$', views.secondView, name='secondview'),
	url(r'^recipes/$', views.recipes, name='recipes'),
	]
