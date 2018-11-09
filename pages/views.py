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

from django.template.loader import render_to_string ## test

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
	template_name = 'about.html'
	

class FlightsEngineView(TemplateView):
	template_name = 'Flights.html'

class HotelsEngineView(TemplateView):
	template_name = 'Hotels.html'
	
class myELYSPageView(TemplateView):
	template_name = 'myELYS.html'
	
def MaxMinPrice(FlightMatrix):
	Prices = []
	for R in range(len(FlightMatrix)):
		Prices.append(FlightMatrix[R]['TPrice']['EUR'])
	MaxPrice = max(Prices)
	MinPrice = min(Prices)
	return(MaxPrice, MinPrice)
	
def MaxMinTime(FlightMatrix, Return):
	TTime = []
	for R in range(len(FlightMatrix)):
		VarTime = (FlightMatrix[R]['FlightTimes']['OutboundT']).split()[0]
		TTime.append(int((VarTime)[0:(len(VarTime)-1)]))
	MaxTTime = max(TTime)+1
	MinTTime = min(TTime)
	return(MaxTTime, MinTTime)

def GenerateFlightMatrix(Origin, Destination, Departure, Return):
## Generating the Request URL with User Choices
	if Return:
		url = ("https://api.skypicker.com/flights?flyFrom=" + Origin + "&to=" + Destination + \
		"&dateFrom=" + Departure + "&dateTo=" + Departure + '&limit=3' + '&sort=quality' + \
		"&returnTo=" + Return + "&returnFrom=" + Return)
	else:
		url = ("https://api.skypicker.com/flights?flyFrom=" + Origin + "&to=" + Destination + \
		"&dateFrom=" + Departure + "&dateTo=" + Departure + '&limit=3' + '&sort=quality')
	
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
	
	def NumberOfFlights(Options, Return):
		for R in range(len(data["data"][Options]["route"])):
			if data["data"][Options]["route"][R]['flyTo'] == Destination:
				if R == 0:
					OutboundFlights = [0]
				else:
					OutboundFlights = [0,R]
			if Return:
				if data["data"][Options]["route"][R]['flyTo'] == Origin:
					if R == max(OutboundFlights)+1:
						InboundFlights = [R]
					else:
						InboundFlights = [max(OutboundFlights)+1,R]
			else:
				InboundFlights = ""
		return OutboundFlights, InboundFlights
	
	def DepartureAirport(Options, Route):
		return(data["data"][Options]["route"][Route]["cityFrom"],data["data"][Options]["route"][Route]["flyFrom"])
	
	def ArrivalAirport(Options, Route):
		return(data["data"][Options]["route"][Route]["cityTo"],data["data"][Options]["route"][Route]["flyTo"])
	
	def TotalPrice(Options):
		return(data["data"][Options]["conversion"])
	
	def TotalFlightTimes(Options, Return):
		OutboundFlights, InboundFlights = NumberOfFlights(Options, Return)
		OutboundTimesR = []; OutboundTimes = []; OutboundRoute = []
		InboundTimes = []; InboundTimesR = []; InboundRoute = []
		OutboundTotal = (data["data"][Options]["fly_duration"])
		if Return:
			InboundTotal = (data["data"][Options]["return_duration"])
		else:
			InboundTotal = ""
		for R in range(max(OutboundFlights)):
			if R > min(OutboundFlights):
				OutboundTimesR.append(data["data"][Options]["route"][R]["dTimeUTC"] - data["data"][Options]["route"][R-1]["aTimeUTC"])
			OutboundTimesR.append(data["data"][Options]["route"][R]["aTimeUTC"] - data["data"][Options]["route"][R]["dTimeUTC"])
		if Return:
			for R in range(max(OutboundFlights)+1, max(InboundFlights)):
				if R > min(InboundFlights):
					InboundTimesR.append(data["data"][Options]["route"][R]["dTimeUTC"] - data["data"][Options]["route"][R-1]["aTimeUTC"])
				InboundTimesR.append(data["data"][Options]["route"][R]["aTimeUTC"] - data["data"][Options]["route"][R]["dTimeUTC"])        
		else:
			InboundTimesR = ''
		for R in OutboundTimesR:
			OutboundTimes.append(datetime.utcfromtimestamp(R).strftime('%Hh %Mm'))
		for R in InboundTimesR:
			InboundTimes.append(datetime.utcfromtimestamp(R).strftime('%Hh %Mm'))
		return {'OutboundT' : OutboundTotal, 'InboundT' : InboundTotal,
				'OutboundRTimes' : OutboundTimes, 'InboundRTimes' : InboundTimes}
	
	def RouteMap(Options, Departure, Return):
		OutboundR, InboundR = NumberOfFlights(Options, Return)
		OutRoute = []; InRoute = []; RouteMap = []
		for R in OutboundR:
			OutRoute.append(DepartureAirport(Options, R))
			if (R > min(OutboundR)) & (R<max(OutboundR)):
				if (ArrivalAirport(Options,R) != DepartureAirport(Options,R+1)):
					OutRoute.append(ArrivalAirport(Options, R))
		OutRoute.append(ArrivalAirport(Options, max(OutboundR)))
		if Return:
			for R in InboundR:
				InRoute.append(DepartureAirport(Options, R))
				if (R > min(InboundR)) & (R < max(InboundR)):
					if(ArrivalAirport(Options,R) != DepartureAirport(Options,R+1)):
						InRoute.append(DepartureAirport(Options, R+1))
			InRoute.append(ArrivalAirport(Options,len(data["data"][Options]["route"])-1))
		return{'OutRoute' : OutRoute, 'InRoute' : InRoute}						
					
	FlightMatrix = []
	for Options in range(len(data["data"])):
		FlightDict = {}
		Leg = []; Outbound = [];  Inbound = []
		FlightDict['Option']=Options+1
		RangeOfFlights = NumberOfFlights(Options, Return) 
		FlightDict['NFlight'] = RangeOfFlights
		for Route in RangeOfFlights[0]:
			#Airline
			Outbound.append({'DTime' : DepartureTime(Options,Route),
					'DAirport' : DepartureAirport(Options, Route),
					'ATime' : ArrivalTime(Options,Route),
					'AAirport' : ArrivalAirport(Options,Route),
					'DDate': DepartureDate(Options,Route)
					})
		if Return:	
			for Route in RangeOfFlights[1]:
				Inbound.append({'DTime' : DepartureTime(Options,Route),
						'DAirport' : DepartureAirport(Options, Route),
						'ATime' : ArrivalTime(Options,Route),
						'AAirport' : ArrivalAirport(Options,Route),
						'DDate': DepartureDate(Options,Route)
						})
		Leg.append({ 'OutboundR': Outbound, 'InboundR': Inbound})
		FlightDict['RMap']=RouteMap(Options, Departure, Return)
		FlightDict['Legs'] = Leg
		FlightDict['TPrice']=TotalPrice(Options)
		FlightDict['FlightTimes']=TotalFlightTimes(Options, Return)
		FlightDict['ArrivalTime_Outbound'] = ArrivalTime(Options,max(RangeOfFlights[0]))
		FlightDict['ArrivalTime_Inbound'] = ArrivalTime(Options,max(RangeOfFlights[1]))
		FlightMatrix.append(FlightDict)
	
	MaxPrice, MinPrice = MaxMinPrice(FlightMatrix)
	MaxTTime, MinTTime = MaxMinTime(FlightMatrix, Return)
	
	return(FlightMatrix, MaxPrice, MinPrice, MaxTTime, MinTTime)
	
def FilterFlights(FlightMatrix, MaxRange, MinRange, MaxTime, MinTime):
	Repeats = []
	if not MaxTime:
		MaxTime = 100000
	if not MinTime:
		MinTime = 0
	if not MaxRange:
		MaxRange = 100000
	if not MinRange:
		MinRange = 0
	for Options in range(len(FlightMatrix)):
		VarTime = FlightMatrix[Options]['TFlightTime'].split()[0]
		if FlightMatrix[Options]['TPrice']['EUR'] > int(MaxRange) :
			Repeats.append(Options)
		if FlightMatrix[Options]['TPrice']['EUR'] < int(MinRange) :
			Repeats.append(Options)
		if int((VarTime)[0:(len(VarTime)-1)]) >= int(MaxTime) :
			Repeats.append(Options)
		if int((VarTime)[0:(len(VarTime)-1)]) < int(MinTime) :
			Repeats.append(Options)
	Repeats = list(set(Repeats))
	Repeats.reverse()
	for R in Repeats:
		del FlightMatrix[R]
	return (FlightMatrix)


def SearchEngine(request):
	# defining the variable
	if request.method == 'GET':
		form = FlightSearchForm()
	elif request.method == 'POST' and "Search" in request.POST:
		form = FlightSearchForm(request.POST)
		if form.is_valid():
			Origin = form.cleaned_data['Origin']
			Destination = form.cleaned_data['Destination']
			DepartureD = form.cleaned_data['Departure']
			ReturnD = form.cleaned_data['Return']	
			Departure =  DepartureD.strftime("%d/%m/%Y")
			if not ReturnD:
				Return = ''
			else:
				Return =  ReturnD.strftime("%d/%m/%Y")
				
			FlightMatrix, MaxPrice, MinPrice, MaxTTime, MinTTime = GenerateFlightMatrix(Origin, Destination, Departure, Return)
			
			request.session['FlightMatrix'] = FlightMatrix
			request.session['Origin'] = Origin
			request.session['Destination'] = Destination
			request.session['Departure'] = Departure
			request.session['Return'] = Return
			
			# passing the variable to the viewitems
			return render(request, 'Flights.html', {
				'Origin' : Origin,
				'Destination' : Destination,
				'Departure' : Departure,
				'FlightMatrix' : FlightMatrix,
				'Return' : Return,
				'MaxPrice' : MaxPrice,
				'MinPrice' : MinPrice,
				'MaxTTime' : MaxTTime,
				'MinTTime' : MinTTime,
				})
				
		return render(request, "Flights.html", {'form': form})
				
	elif request.method == 'POST' and "Filter" in request.POST:
		form = FlightSearchForm(request.POST)
		if form.is_valid():
			MinRange = form.cleaned_data['Min_P']
			MaxRange = form.cleaned_data['Max_P']
			MinTime = form.cleaned_data['Min_T']
			MaxTime = form.cleaned_data['Max_T']
			
			FlightMatrix = request.session['FlightMatrix']
			
			MaxPrice, MinPrice = MaxMinPrice(FlightMatrix)
			MaxTTime, MinTTime = MaxMinTime(FlightMatrix)
			FlightMatrix = FilterFlights(FlightMatrix, MaxRange, MinRange, MaxTime, MinTime)
			
			MinRange, MaxRange, MinTime, MaxTime = ['' if var is None else var for var in [MinRange, MaxRange, MinTime, MaxTime]]
						
			return render(request, 'Flights.html', {
					'FlightMatrix' : FlightMatrix,
					'Origin' : request.session['Origin'],
					'Destination' : request.session['Destination'],
					'Departure' : request.session['Departure'],
					'Return': request.session['Return'],
					'MaxRange' : MaxRange,
					'MinRange' : MinRange,
					'MaxTime' : MaxTime,
					'MinTime' : MinTime,
					'MaxPrice' : MaxPrice,
					'MinPrice' : MinPrice,
					'MaxTTime' : MaxTTime,
					'MinTTime' : MinTTime,
					})
				
		return render(request, "Flights.html", {'form': form})
		
	else:
		form = FlightSearchForm(request.POST)
		print("Good Too")
		return render(request, "Flights.html", {'form': form})
	
	return render(request, "Flights.html", {'form': form})

