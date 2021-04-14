from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

#UserCreationForm is inherited in this class. This helps us extend the usercreation form to add other fields i.e email
class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(required=True)

	#this class function takes the username and converts it to a lower case insensitive char and saves to the database 
	def clean_username(self):
		data = self.cleaned_data['username']
		return data.lower()

	#the meta class makes it possible to edit the UserCreationForm with more fields 
	class Meta:
		model = User # User model to be affected 
		fields = ['username', 'email', 'password1', 'password2']

	def clean_email(self):
		email = self.cleaned_data['email']
		username = data = self.cleaned_data['username']
		# print User.objects.filter(email=email).count()
		if email and User.objects.filter(email__iexact=email).exists():
			raise forms.ValidationError('This email address is already registered.')
		return email


""" UserLoginForm inherits from the django AuthenticationForm 
done here in other to changed the cleaned username to lower the case to authenticate the user(for now). 
"""
class UserLoginForm(AuthenticationForm):

	class Meta:
		model = User
		fields = ['username', 'password']

	def clean_username(self):
		data = self.cleaned_data['username']
		return data.lower() #converts the username to lower case for authenticaton.

#this class helps to update the user model form i.e editing the username and email
class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	#the meta class makes it possible to edit update the fields in user form
	class Meta:
		model = User # User model to be affected 
		fields = ['username', 'email']

	def clean_username(self):
		data = self.cleaned_data['username']
		return data.lower() 

#this class helps to update the profile model form i.e editing the image field
class ProfileUpdateForm(forms.ModelForm):
	#the meta class makes it possible to edit update the fields in profile form
	class Meta:
		model = Profile # Profile model to be affected 
		fields = ['first_name','last_name','gender','location','bio','image']

#this class displays the profile form to be updated by the user. 
class CreateProfileForm(forms.ModelForm):
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	GENDER_SELECT = [('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ]
	gender = forms.ChoiceField(choices=GENDER_SELECT, widget=forms.RadioSelect())

	class Meta: 
		model = Profile
		fields = ['first_name', 'last_name', 'gender']
		# GENDER_SELECT = (('M', 'Male'), ('F', 'Female'), ('O', 'Other'), )
		# widgets = {'gender': forms.RadioSelect(choices=GENDER_SELECT)}