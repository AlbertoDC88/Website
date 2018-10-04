## Python Code Imports
import urllib.request
import json
from pprint import pprint
from datetime import datetime, date, time

## Django Code Imports
from django.views.generic import TemplateView
from .forms import FlightSearchForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
	template_name = 'about.html'
	
class TravelPageView(TemplateView):
	template_name = 'TravelSearch.html'

class FlightsEngineView(TemplateView):
	template_name = 'Flights.html'

class HotelsEngineView(TemplateView):
	template_name = 'Hotels.html'
	

def SearchEngine(request):
	# defining the variable
	if request.method == 'GET':
		form = FlightSearchForm()
	else:
		form = FlightSearchForm(request.POST)
		if form.is_valid():
			Origin = form.cleaned_data['Origin']
			Destination = form.cleaned_data['Destination']
			Departure = form.cleaned_data['Departure']
			
			## Generating the Request URL with User Choices
			url = ("https://api.skypicker.com/flights?flyFrom=" + Origin + "&to=" + Destination + \
			"&dateFrom=" + Departure + "&dateTo=" + Departure + '&limit=20' + '&sort=quality')
			
			## Receiving the Response from API
			response = urllib.request.urlopen(url)
			
			## Runing the Responses and Removing failed responses
			with response as f:
				data = json.load(f)
				Repeats = []
				for Options in range(len(data["data"])):
					if data["data"][Options]["flyTo"] != Destination:
						Repeats.append(Options)
				Repeats.reverse()
				for R in Repeats:
					del data["data"][R]
			
			## Open Airlines Dictionary
			def DepartureTime(Options, Route):
				return(datetime.utcfromtimestamp(data["data"][Options]["route"][Route]["dTime"]).strftime('%H:%M'))
    
			def ArrivalTime(Options, Route):
				return(datetime.utcfromtimestamp(data["data"][Options]["route"][Route]["aTime"]).strftime('%H:%M'))
			
			def DepartureDate(Options, Route):
				return(datetime.utcfromtimestamp(data["data"][Options]["route"][Route]["dTime"]).strftime('%A %d of %B'))
			
			def NumberOfFlights(Options):
				return(len(data["data"][Options]["route"]))
			
			def DepartureAirport(Options, Route):
				return(data["data"][Options]["route"][Route]["cityFrom"],data["data"][Options]["route"][Route]["flyFrom"])
			
			def ArrivalAirport(Options, Route):
				return(data["data"][Options]["route"][Route]["cityTo"],data["data"][Options]["route"][Route]["flyTo"])
			
			def TotalPrice(Options):
				return(data["data"][Options]["conversion"])
			
			def TotalFlightTime(Options):
				return(data["data"][Options]["fly_duration"])
			
			def RouteMap(Options):
				Trip = []
				Trip.append(DepartureAirport(Options, 0))
				for R in range(len(data["data"][Options]["route"])-1):
					Trip.append(ArrivalAirport(Options, R))
					if ArrivalAirport(Options,R) != DepartureAirport(Options,R+1):
						Trip.append(DepartureAirport(Options, R+1))
				Trip.append(ArrivalAirport(Options,len(data["data"][Options]["route"])-1))
				return(str(Trip))	
							
			def MaxMinPrice():
				Prices = []
				for R in range(len(data["data"])):
					Prices.append(FlightMatrix[R]['TPrice']['EUR'])
				MaxPrice = max(Prices)
				MinPrice = min(Prices)
				return(MaxPrice, MinPrice)
							
			FlightMatrix = []
			for Options in range(len(data["data"])):
				FlightDict = {}
				Legs = []
				FlightDict['Option']=Options+1
				FlightDict['NFlight']=NumberOfFlights(Options)
				for Route in range(len(data["data"][Options]["route"])):
					#Airline
					Legs.append({'DTime' : DepartureTime(Options,Route),
                     'DAirport' : DepartureAirport(Options, Route),
                     'ATime' : ArrivalTime(Options,Route),
                     'AAirport' : ArrivalAirport(Options,Route),
                     'DDate': DepartureDate(Options,Route)
                     })
				FlightDict['RMap']=RouteMap(Options)
				FlightDict['Leg'] = Legs
				FlightDict['TPrice']=TotalPrice(Options)
				FlightDict['TFlightTime']=TotalFlightTime(Options)
				FlightMatrix.append(FlightDict)
			
			MaxPrice, MinPrice = MaxMinPrice()
			
			# passing the variable to the viewitems
			return render(request, 'Flights.html', {
				'Origin' : Origin,
				'Destination' : Destination,
				'Departure' : Departure,
				'FlightMatrix' : FlightMatrix,
				'MaxPrice' : MaxPrice,
				'MinPrice' : MinPrice,
				})
	return render(request, "Flights.html", {'form': form})

