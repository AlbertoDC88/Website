# sendemail/forms.py
from django import forms

class FlightSearchForm(forms.Form):
	Origin = forms.CharField(required=False)
	Destination = forms.CharField(required=False)
	Departure = forms.DateField(required=False)
	Return = forms.DateField(required=False)
	Min_P = forms.IntegerField(required=False)
	Max_P = forms.IntegerField(required=False)#
	Min_T = forms.IntegerField(required=False)
	Max_T = forms.IntegerField(required=False)#
	
	