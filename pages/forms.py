# sendemail/forms.py
from django import forms

class FlightSearchForm(forms.Form):
	Origin = forms.CharField(required=False)
	Destination = forms.CharField(required=False)
	Departure = forms.CharField(required=False)
	Return = forms.CharField(required=False)
	Min_P = forms.IntegerField(required=False)
	Max_P = forms.IntegerField(required=False)#
	Min_T = forms.IntegerField(required=False)
	Max_T = forms.IntegerField(required=False)#