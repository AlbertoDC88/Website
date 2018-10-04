# sendemail/forms.py
from django import forms

class FlightSearchForm(forms.Form):
	Origin = forms.CharField(required=False)
	Destination = forms.CharField(required=False)
	Departure = forms.CharField(required=False)
	Min_P = forms.CharField(required=False)
	Max_P = forms.CharField(required=False)#
