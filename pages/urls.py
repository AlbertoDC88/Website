# pages/urls.py
from django.urls import path
from django.views.generic.base import TemplateView
from .views import HomePageView, AboutPageView, TravelPageView, HotelsEngineView, FlightsEngineView, SearchEngine

urlpatterns = [
	path('about/', AboutPageView.as_view(), name='about'),
    path('', HomePageView.as_view(), name='home'),
	path('TravelSearch/', TravelPageView.as_view(), name='TravelSearch'),
	path('TravelSearch/Hotels/', HotelsEngineView.as_view(), name='Hotels'),
	path('TravelSearch/Flights/', SearchEngine, name='Flights'),
]