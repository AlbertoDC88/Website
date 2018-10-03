# sendemail/forms.py
from django import forms

class FlightSearchForm(forms.Form):
	Origin = forms.CharField(required=True)
	Destination = forms.CharField(required=True)
	Departure = forms.CharField(required=True)