from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views import View
from .models import Activity
from .forms import ActivityForm
from blog.models import Post
from relationships.models import Relationship
from blog.forms import PostForm
from django.urls import reverse

# Create your views here.

# class ActivityCreateView(CreateView):
# 	model = Activity # model to be affected
# 	# fields = ['name', 'description', 'category', 'target'] # fields to be updated
# 	form_class = ActivityForm
# 	template_name = 'activity/activity_create.html'

# 	def form_valid(self, form):
# 		form.instance.author = self.request.user
# 		return super().form_valid(form)

def CreateActivity(request):
	if request.method == 'POST':
		form = ActivityForm(request.POST)
		if form.is_valid():
			form.instance.author = request.user
			new_form = form.save()
			username = form.cleaned_data.get('author')
			return redirect('activity:activity-list', request.user)
	else:
		form = ActivityForm()

	context= {
		'form': form
	}

	return render(request, 'activity/activity_create.html', context)



class ActivityListView(ListView):
	model = Activity # model to be affected
	template_name = 'activity/activity_list.html' #<app>/<model>_<viewtype>.html
	context_object_name = 'activities' #by default it expects the context to be called object here it is changed to posts as above.
	ordering = ['-date_posted'] #this orders the post in ascending order (most recent post to older post)
	paginate_by = 5 #reduces the amount of posts displayed per page

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username')) 
		return Activity.objects.filter(author=user).order_by('-date_posted') # the activity model object is filtered to return only posts from a certain  user
	
	""" the get_context_data function of the listview class is overriden to return an instance of the user object """
	def get_context_data(self, **kwargs):
		context = super(ActivityListView, self).get_context_data(**kwargs) 
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		posts = Post.objects.filter(author=user).count()
		activities = Activity.objects.filter(author=user).count()
		following  = Relationship.objects.filter(from_user=user).count()
		followers  = Relationship.objects.filter(to_user=user).count()
		context['posts_count'] = posts
		context['activities_count'] = activities
		context['following_count'] = following
		context['followers_count'] = followers  
		context['user_profile'] = user #saves the user object as user_profile
		return context

class ActivityPostListView(ListView):
	model = Activity # model to be affected
	context_object_name = 'activity'
	template_name = 'activity/activity_post_detail.html'
	# ordering = ['-date_posted']
	paginate_by = 10
	
	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		post = get_object_or_404(Activity, pk=self.kwargs.get('pk'), slug=self.kwargs.get('slug')) 
		return Post.objects.filter(author=user, activity=post)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs) 
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		activity = get_object_or_404(Activity, pk=self.kwargs.get('pk'))
		posts = Post.objects.filter(author=user).count()
		activities = Activity.objects.filter(author=user).count()
		following  = Relationship.objects.filter(from_user=user).count()
		followers  = Relationship.objects.filter(to_user=user).count()
		context['posts_count'] = posts
		context['activities_count'] = activities
		context['following_count'] = following
		context['followers_count'] = followers  
		context['user_profile'] = user #saves the user object as user_profile
		context['activities'] = activity
		context['is_liked'] = Post.objects.filter(likes__username=self.request.user.username).values_list('id', flat=True)
		context['is_favorite'] = Post.objects.filter(favorite__username=self.request.user.username).values_list('id', flat=True)
		is_bookmarked = False
		if activity.bookmark.filter(pk=user.id).exists():
			is_bookmarked = True
		context['is_bookmarked'] = is_bookmarked
		return context


class ActivityDetailView(DetailView):
	model = Activity # model to be affected

class ActivityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Activity # model to be affected
	fields = ['name', 'description', 'target'] # fields to be updated
	template_name = 'activity/activity_create.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object() #get_object is a method of the UpdateView which gets the post object
		if self.request.user == post.author: # if the logged in user is the author of the post trying to be updated
			return True
		return False

class ActivityDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Activity # model to be affected

	def get_success_url(self):
		activity = self.object.author
		# activity_slug = self.object.slug
		return reverse('activity-list', kwargs={'username': activity})

	def test_func(self):
		activity = self.get_object() #get_object is a method of the UpdateView which gets the post object
		if self.request.user == activity.author: # if the logged in user is the author of the post trying to be updated
			return True
		return False

def bookmark_activity(request, pk):
	activity = get_object_or_404(Activity, pk=pk)

	if activity.bookmark.filter(id=request.user.id).exists():
		activity.bookmark.remove(request.user)
	else: 
		activity.bookmark.add(request.user)
	return HttpResponseRedirect(activity.get_absolute_url())

def bookmarks(request):
	user = request.user
	bookmark_activity = user.bookmark.all().order_by('-id') 

	context={
		'bookmark_activity': bookmark_activity,
		'user_profile': user
		}

	return render(request, 'activity/bookmarks.html', context)