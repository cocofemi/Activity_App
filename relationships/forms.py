from django import forms
from .models import Relationship


class SearchForm(forms.Form):
	q = forms.CharField(label='', max_length=50)