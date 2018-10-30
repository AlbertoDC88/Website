# pages/urls.py
from django.urls import path
from django.views.generic.base import TemplateView
from .views import myELYSPageView, HomePageView, AboutPageView, HotelsEngineView, FlightsEngineView, SearchEngine

urlpatterns = [
	path('about/', AboutPageView.as_view(), name='about'),
	path('MyELYS/', myELYSPageView.as_view(), name='myELYS'),
    path('', HomePageView.as_view(), name='home'),
	path('MyELYS/Hotels/', HotelsEngineView.as_view(), name='Hotels'),
	path('MyELYS/Flights/', SearchEngine, name='Flights'),
]