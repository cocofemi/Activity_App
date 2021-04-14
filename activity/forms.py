from django import forms
from .models import Activity
from .widgets import FengyuanChenDatePickerInput
import datetime

class ActivityForm(forms.ModelForm):
	name		= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Give a name to the activity you want to start'}))
	description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'rows':4, 'placeholder':'Give a brief description of the activity you want to start'}))
	# target		= forms.CharField(label='Target', widget=forms.Textarea(attrs={'placeholder':'What do you aim to achieve at the end of your activity'}))
	start_date	= forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(attrs={'placeholder':'Select a start date'}))
	end_date	= forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(attrs={'placeholder':'Select an end date'}))
	image = forms.ImageField(label='', required=False)
	CATEGORY_SELECT = (('', 'Choose a category'), ('Arts', 'Arts'), ('Adventure', 'Adventure'), 
		('Business', 'Business'), ('Design', 'Design'), ('Entertainment', 'Entertainment'), ('Education', 'Education'), 
		('Health', 'Health'), ('Fitness', 'Fitness'), 
		('Fashion', 'Fashion'), ('Food', 'Food'), ('Music', 'Music'), ('Programming', 'Programming'), ('Startup', 'Startup'),
		('Technology', 'Technology'), ('Other', 'Other'), )
	category = forms.ChoiceField(label='', choices=CATEGORY_SELECT, widget=forms.Select(attrs={'empty_label': 'Choose a category'}))

	class Meta:
		model = Activity
		fields = ['name','description', 'category', 'image','start_date','end_date']

	def clean_start_date(self):
		start_date = self.cleaned_data['start_date']
		if start_date < datetime.date.today():
			raise forms.ValidationError("Start date cannot be in the past")
		return start_date

	def clean_end_date(self):
		end_date = self.cleaned_data['end_date']
		if end_date < datetime.date.today():
			raise forms.ValidationError("End date cannot be in the past")
		return end_date