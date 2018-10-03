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
	#number = 6
	#origin = "Origin Airport"
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
			"&dateFrom=" + Departure + "&dateTo=" + Departure + '&limit=20')
			
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
			##with open('Airlines.txt','r') as inf:
				##dict_from_file = eval(inf.read())
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
							
			FlightMatrix = []
	
			for Options in range(len(data["data"])):
				FlightDict = {}
				FlightDict['Option']=Options+1
				FlightDict['NFlight']=NumberOfFlights(Options)
				for Route in range(len(data["data"][Options]["route"])):
					#Airline
					FlightDict['DTime']=DepartureTime(Options,Route)
					FlightDict['DAirport']=DepartureAirport(Options, Route)
					FlightDict['ATime']=ArrivalTime(Options,Route)
					FlightDict['AAirport']=ArrivalAirport(Options,Route)
					FlightDict['DDate']=DepartureDate(Options,Route)
					FlightDict['RMap']=RouteMap(Options)
				FlightDict['TPrice']=TotalPrice(Options)
				FlightDict['TFlightTime']=TotalFlightTime(Options)
				FlightMatrix.append(FlightDict)
			
			# passing the variable to the viewitems
			return render(request, 'Flights.html', {
				'Origin' : Origin,
				'Destination' : Destination,
				'Departure' : Departure,
				'FlightMatrix' : FlightMatrix
				
				#'Option' : Option,
				#'NumberOfFlights': NFlights,
				#'Airline': Airline,
				#'DepartureTime': DTime,
				#'DepartureAirport': DAirport,
				#'ArrivalTime' : ATime,
				#'ArrivalAirport': AAirport,
				#'DepartureDate': DDate,
				#'RouteMap': RMap,
				#'TotalPrice': TPrice,
				#'TotalFlightTime' : TFlightTime,
				})
	return render(request, "Flights.html", {'form': form})

