from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserLoginForm, CreateProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
# Create your views here.

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST) #UserRegisterForm(subclassed form of UserCreationForm which is an auto-generated form from python)
		if form.is_valid():
			new_user = form.save()
			username = form.cleaned_data.get('username')
			login(request, new_user) # the user is automatically logged in after registration
			return redirect('signup_profile') #redirects to the create profile page
	else:
		form = UserRegisterForm() #UserRegisterForm is an auto-generated form from python

	return render(request, 'users/register.html', {'form': form})


"""
the UserUpdateForm and the UserRegisterForm are populated with the user data(instance=request.user)

and the data to be posted(request.POST)

the request.FILES sends the image contained in the post to the ProfileUpdateForm
"""
@login_required #this a decorator(a decorator adds functionality to an existing function)
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user) #we instantiate the UserUpdateForm in order to use it in the template
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated')
			return redirect('edit-profile') #redirects to the profile page
	else:
		u_form = UserUpdateForm(instance=request.user) #we instantiate the UserUpdateForm in order to use it in the template
		p_form = ProfileUpdateForm(instance=request.user.profile)

	#pass the instance so we can render it in the template
	context = {
		'u_form': u_form,
		'p_form': p_form
	}
	return render(request, 'users/editprofile.html', context)

"""
this LoginView function subclasses the LoginView class based view of django.

done here in other to use the UserLoginForm which is a subclass of the django AuthenticationForm
"""	
class LoginView(LoginView):
	template_name = 'users/login.html'
	form_class = UserLoginForm

"""
this function view takes care of updating the user's profile after registration
"""
@login_required
def registerProfile(request):
	if request.method == 'POST':
		form = CreateProfileForm(request.POST, instance=request.user.profile)
		if form.is_valid():
			form.save()
			messages.success(request, f'Your account has been created')
			return redirect('post:blog-home') # redirects to the homepage on success.
	else:
		form = CreateProfileForm()

	return render(request, 'users/signup_profile.html', {'form': form})