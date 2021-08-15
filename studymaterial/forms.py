from django import forms
from django.forms import widgets
from . models import *
class DashboardFom(forms.Form):
	text = forms.CharField(max_length=100,label="Enter your search:")