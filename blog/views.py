from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views import View
from django.template.loader import render_to_string 
from .models import Post
from comments.forms import CommentForm
from activity.models import Activity
from relationships.models import Relationship
from relationships.util import get_people_user_follows
from comments.models import Comment
from users.forms import UserLoginForm
from django.contrib.auth.views import LoginView
from .forms import PostForm
from relationships.forms import SearchForm
from django.urls import reverse
from activity.views import ActivityPostListView
from itertools import chain
from operator import attrgetter
from notify.signals import notify
from dal import autocomplete
import json
#from django.http import HttpResponse
# Create your views here.

@login_required
def home(request):
	"""this function renders the home html template in templates directory(using the render import)"""

	user_followers = Relationship.objects.filter(from_user=request.user).values_list('to_user', flat=True)
	user_following = Relationship.objects.filter(to_user=request.user).values_list('from_user', flat=True)
	posts = Post.objects.filter(author_id__in=user_followers).order_by('-date_posted') | Post.objects.filter(author=request.user).order_by('-date_posted') | Post.objects.filter(author_id__in=user_following).order_by('-date_posted')#query's the database for the all the posts
	users = User.objects.all().order_by('-date_joined')[:6]
	#user = get_object_or_404(User, username=request.user)
	user_posts = posts.filter(author=request.user).count()
	user_activity  = Activity.objects.filter(author=request.user).count()
	user_following = Relationship.objects.filter(from_user=request.user).count()
	user_followers = Relationship.objects.filter(to_user=request.user).count()

	search_form = SearchForm

	return_list = []
	for post in posts:
		return_list.append((post, Post.objects.filter(id=post.id, likes__username=request.user.username), 
			Post.objects.filter(id=post.id, favorite__username=request.user.username)))

	# is_favorite = posts.filter(favorite__username=request.user.username).values_list('id', flat=True)
	# is_liked	= posts.filter(likes__username=request.user.username).values_list('id', flat=True)
	
	# activities = Activity.objects.all()
	# result_list = sorted(chain(posts, activities), key=attrgetter('date_posted'), reverse=True)
	# filter(author_id__in=following)

	if request.method == 'POST':
		form = PostForm(request.user, request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.activity_id = form.cleaned_data['activity'].pk
			post.save()
			return redirect('post:blog-home')
	else:
		form = PostForm(user=request.user)

	context = {
		'posts': return_list, #query's the database for the all the posts
		'users': users,
		# 'activities': Activity.objects.all().order_by('-date_posted'),
		# 'posts': result_list,
		'form': form,
		'posts_count': user_posts,
		'activities_count': user_activity,
		'following_count' : user_following,
		'followers_count' : user_followers,
		# 'is_liked': is_liked,
		# 'is_favorite': is_favorite,
		'search_form': search_form
	}
	return render(request, 'blog/home.html', context);


#this function renders the about html template in templates directory
class IndexView(LoginView):
	template_name = 'users/index_login.html'
	form_class = UserLoginForm

#this function renders the about html template in templates directory
def about(request):
	return render(request, 'blog/about.html', {'title': 'About'});


# class PostListView(ListView):
# 	"""A class-based view to display the posts in a list view
# 	the class is inherited from the listview view class of django
# 	django expects to look for the template in this pattern(#<app>(name of the app)/<model>(model name)_<viewtype>(type of view i.e create, detail).html)
# 	"""
# 	model = Post # model to be affected
# 	template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
# 	context_object_name = 'posts' #by default it expects the context to be called object here it is changed to posts as above.
# 	ordering = ['-date_posted'] #this orders the post in ascending order (most recent post to older post)
# 	paginate_by = 5 #reduces the amount of posts displayed per page

	# def get_queryset(self):
	# 	qs1 = Post.objects.all()
	# 	qs2 = Activity.objects.all()
	# 	queryset = sorted(chain(qs1, qs2), key=attrgetter('date_posted'),reverse=True)
	# 	return queryset

	# def get_context_data(self, **kwargs):
	# 	context = super(PostListView, self).get_context_data(**kwargs)
	# 	# posts = Post.objects.all()
	# 	context['activities'] = Activity.objects.all()
	# 	# context['queryset'] = sorted(chain(posts, activities), key=attrgetter('date_posted'), reverse=True)
	# 	return context

# class UserPostListView(ListView, FormMixin):
# 	model = Post # model to be affected
# 	template_name = 'blog/user_posts.html' #<app>/<model>_<viewtype>.html
# 	context_object_name = 'posts' #by default it expects the context to be called object here it is changed to posts as above.
# 	paginate_by = 8 #reduces the amount of posts displayed per page
# 	slug_field = 'user__username'
# 	slug_url_kwarg = 'username'
# 	form_class = PostForm
# 	ordering = '-date_posted'

# 	def get_queryset(self):
# 		""" the get_queryset method(from the class listview)here is overriden to return the username in the url pattern
# 		username=self.kwargs.get('username') gets the username from the url or returns a 404(does not exist)
# 		"""
# 		user = get_object_or_404(User, username=self.kwargs['username']) 
# 		return Post.objects.filter(author=user).order_by('-date_posted') # the post model object is filtered to return only posts from a certain  user
	
# 	def get_context_data(self, **kwargs):
# 		""" the get_context_data function of the listview class is overriden to return an instance of the user object """

# 		context = super(UserPostListView, self).get_context_data(**kwargs) 
# 		user = get_object_or_404(User, username=self.kwargs.get('username')) #get the username from the url
# 		posts = Post.objects.filter(author=user).count()
# 		activities = Activity.objects.filter(author=user).count()
# 		following  = Relationship.objects.filter(from_user=user).count()
# 		followers  = Relationship.objects.filter(to_user=user).count()
# 		context['posts_count'] = posts
# 		context['activities_count'] = activities
# 		context['following_count'] = following
# 		context['followers_count'] = followers
# 		context['user_profile'] = user #saves the user object as user_profile
# 		context['is_favorite'] = Post.objects.filter(favorite__username=self.request.user.username).values_list('id', flat=True)
# 		context['is_liked'] = Post.objects.filter(likes__username=self.request.user.username).values_list('id', flat=True)
# 		return context

# 	def get_form_kwargs(self):
# 		kwargs = super(UserPostListView,self).get_form_kwargs()
# 		kwargs.update({'user': self.request.user})
# 		return kwargs

def PostDetail(request, pk, username): 
	"""
	a view function to display a post in detail with all its comments and replies
	a comment form is also passed for a user to leave a comment
	"""
	post = get_object_or_404(Post, pk=pk) #get a single post using its pk
	user = get_object_or_404(User, username=username)
	is_favorite = False
	is_liked	= False
	comment_like= False

	if post.likes.filter(pk=request.user.id).exists():
		is_liked = True

	if post.favorite.filter(pk=request.user.id).exists():
		is_favorite = True 

	# filter the comment model returning all comments associated with an individual post 
	comment_post = Comment.objects.filter(post=pk, parent__isnull=True).order_by('date_posted') 

	comment_like = comment_post.filter(likes__username=request.user.username).values_list('id', flat=True)

	if request.method == 'POST':
		comment_form = CommentForm(request.POST, request.FILES or None)
		if comment_form.is_valid():
			Parent_obj = None
			try:
				Parent_id = int(request.POST.get('parent_id')) #get the id of the form 
			except:
				Parent_id = None
			if Parent_id: 
				Parent_obj = Comment.objects.get(id=Parent_id) #get the parent obj from the comment model passing in the id value
				if Parent_obj:
					reply_comment = comment_form.save(commit=False) #saves the comment as a reply to another comment on the main post not as a comment on the main post
					reply_comment.author = request.user #saves the author object as the logged in user
					reply_comment.parent = Parent_obj # saves the comment as a reply
					# return redirect('comment:reply-thread', Parent_obj.id)
			comment = comment_form.save(commit=False) # if no parent id is gotten save the comment as a new comment to the main post 
			comment.author = request.user # save username of the logged in user
			comment.post = post # saves the pk of the current post 
			comment.content = comment_form.cleaned_data.get('content')
			# comment.image = comment_form.cleaned_data.get('image')
			notify.send(request.user, recipient=user, actor=request.user, 
				verb='commented on your post', obj=comment.post, nf_type='comment_by_user')
			comment.save()
			parts = comment.content.split()
			for index, value in enumerate(parts):
					if value.startswith("@"):
						results = value[1:]
						try:
							user = User.objects.get(username=results)
							notify.send(request.user, recipient=user, actor=request.user, 
								verb='mentioned you in a comment', target=comment, nf_type='mentioned_comment_by_user')
						except user.DoesNotExist: 
							return redirect('post:post-detail', username, pk)
			return redirect('post:post-detail', username, pk)
	else:
		comment_form = CommentForm() #if no value is gotten return the form

	context = {
		'user_profile': user,
		'object': post,
		'comments': comment_post,
		'comment_form': comment_form,
		'is_favorite': is_favorite,
		'is_liked': is_liked,
		'comment_like':comment_like,
		'search_form': SearchForm
	}

	return render(request, 'blog/post_detail.html', context);

@login_required
def UserPosts(request, username):
	user = get_object_or_404(User, username=username)
	posts = Post.objects.filter(author=user).order_by('-date_posted')
	following  = Relationship.objects.filter(from_user=user).count()
	followers  = Relationship.objects.filter(to_user=user).count()
	activities = Activity.objects.filter(author=user).count()

	# is_liked  =	False
	# is_favorite = posts.filter(favorite__username=request.user.username).values_list('id', flat=True)

	return_list = []
	for post in posts:
		return_list.append((post, Post.objects.filter(id=post.id, likes__username=request.user.username), 
			Post.objects.filter(id=post.id, favorite__username=request.user.username)))
	# is_liked	= posts.filter(likes__username=request.user.username).values_list('id', flat=True)

	post_form = PostForm(request.user, request.POST, request.FILES)

	# if request.method == 'POST':
	# 	form = PostForm(request.user, request.POST, request.FILES)
	# 	if form.is_valid():
	# 		post = form.save(commit=False)
	# 		post.author = request.user
	# 		post.activity_id = form.cleaned_data['activity'].pk
	# 		post.content = form.cleaned_data['content']
	# 		post.image = form.cleaned_data['image']
	# 		post.save()

	# 		parts = post.content.split()
	# 		for index, value in enumerate(parts):
	# 				if value.startswith("@"):
	# 					results = value[1:]
	# 					try:
	# 						user = User.objects.get(username=results)
	# 						notify.send(request.user, recipient=user, actor=request.user, 
	# 							verb='mentioned you in a post', target=post, nf_type='mentions_by_user')
	# 					except user.DoesNotExist: 
	# 						return redirect('post:post-detail', username, pk)
	# 		return HttpResponseRedirect(post.get_absolute_url())
	# else:
	# 	form = PostForm(user=request.user)

	context = {
		'form': post_form,
		'user_profile': user,
		'posts': return_list,
		'followers_count': followers,
		'following_count': following,
		'activities_count': activities,
		'posts_count': Post.objects.filter(author=user).count(),
		# 'is_liked': is_liked,
		# 'is_favorite': is_favorite,
		'search_form': SearchForm
	}

	return render(request, 'blog/user_posts.html', context)

# class PostCreateView(LoginRequiredMixin, CreateView):

# 	"""
# 	A class-based view to create the posts 
# 	the class is inherited from the CreateView view class of django

# 	LoginRequiredMixin is imported and makes it necessary to be logged in to access this page or create posts

# 	the form_valid method overrides the form method to set the author of the form to the current user.
	
# 	this view uses the template post_form.html
# 	"""

# 	model = Post # model to be affected
# 	form_class = PostForm
# 	# fields = ['title', 'content', 'activity', 'image']

# 	def form_valid(self, form):
# 		form.instance.author = self.request.user
# 		form.instance.activity_id = form.cleaned_data['activity'].pk
# 		form.instance.title = form.cleaned_data['title']
# 		form.instance.content = form.cleaned_data['content']
# 		form.instance.image = form.cleaned_data['image']

# 		# parts = form.instance.content.split()
# 		# for index, value in enumerate(parts):
# 		# 	if value.startswith("@"):
# 		# 		results = value[1:]
# 		# 		user = User.objects.get(username=results)
# 		# 		notify.send(self.request.user, recipient=user, actor=self.request.user, 
# 		# 			verb='mentioned you in a post', target=form, nf_type='mentions_by_user')
# 		return super().form_valid(form)

# 	def get_form_kwargs(self):
# 		kwargs = super(PostCreateView,self).get_form_kwargs()
# 		kwargs.update({'user': self.request.user})
# 		return kwargs

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	"""A class-based view to update a post
	the class is inherited from the UpdateView class of django

	LoginRequiredMixin is imported and makes it necessary to be logged in to access this page or create posts

	UserPassesTestMixin makes it necessary that only a users created post can be updated by them.

	the test_func is a method which checks if the logged in user is the author of the post.

	the form_valid method overrides the form method to set the user name.

	this view uses the template post_form.html
"""
	model = Post # model to be affected
	form_class = PostForm
	template_name = 'blog/edit_post.html'
	# fields = ['title', 'content', 'activity', 'image'] # fields to be updated

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.activity_id = form.cleaned_data['activity'].pk
		# form.instance.title = form.cleaned_data['title']
		form.instance.content = form.cleaned_data['content']
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object() #get_object is a method of the UpdateView which gets the post object
		if self.request.user == post.author: # if the logged in user is the author of the post trying to be updated
			return True
		return False

	def get_form_kwargs(self):
		kwargs = super(PostUpdateView,self).get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	"""A class-based view to delete a post 
	the class is inherited from the DetailView view class of django
"""

	model = Post # model to be affected
	# success_url = 'blog-home'

	def get_success_url(self):
		post = self.object.author
		return reverse('post:user-posts', kwargs={'username': post})

	def test_func(self):
		post = self.get_object() #get_object is a method of the UpdateView which gets the post object
		if self.request.user == post.author: # if the logged in user is the author of the post trying to be updated
			return True
		return False

# class PostListActivityView(View):
# 	def get(self, request, *args, **kwargs):
# 		view = UserPostListView.as_view()
# 		return view(request, *args, **kwargs)

# 	def post(self, request, *args, **kwargs):
# 		view = PostCreateView.as_view()
# 		return view(request, *args, **kwargs)

def favorite_post(request):
	"""
		function view to favorite a post checks if the post has been favorited before if it has the post is unfavorited 
		else the post is favorited
	"""
	post = get_object_or_404(Post, id=request.POST.get('id'))
	is_favorite = False

	if post.favorite.filter(id=request.user.id).exists():
		post.favorite.remove(request.user)
		is_favorite = False
	else:
		post.favorite.add(request.user)
		is_favorite = True
		notify.send(request.user, recipient=post.author, actor=request.user, 
				verb='favorited your post', target=post, nf_type='like_by_user')

	context = {
		'post': post,
		'is_favorite': is_favorite
	}
	if request.is_ajax():
		html = render_to_string('blog/post_favorite_button.html', context, request=request)
		return JsonResponse({'form':html})

def like_post(request):
	"""
		function view to like a post, comment or reply....
	"""
	# post = get_object_or_404(Post, pk=pk)
	post = get_object_or_404(Post, id=request.POST.get('id'))
	is_liked = False

	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		is_liked = False
	else:
		post.likes.add(request.user)
		is_liked = True
		notify.send(request.user, recipient=post.author, actor=request.user, 
				verb='liked your post', target=post, nf_type='like_by_user')

	context = {
		'post': post,
		'is_liked': is_liked
	}
	if request.is_ajax():
		html = render_to_string('blog/post_like_button.html', context, request=request)
		return JsonResponse({'form':html})


def user_favorites(request, username):
	user = request.user
	favorites = user.favorite.all().order_by('-id') 

	is_favorite = favorites.filter(favorite__username=request.user.username).values_list('id', flat=True)
	is_liked	= favorites.filter(likes__username=request.user.username).values_list('id', flat=True)	

	context = {
		'favorites': favorites,
		'user_profile': user,
		'is_favorite': is_favorite,
		'is_liked': is_liked
	}

	return render(request, 'blog/user_favorites.html', context)


# class userAutoCompleteSearch(autocomplete.Select2QuerySetView):
# 	def get_queryset(self): 
# 		if not self.request.user.is_authenticated:
# 			return User.objects.none()

# 		qs = User.objects.all()

# 		if self.q:
# 			qs = qs.filter(username__istartswith=self.q)
# 		return qs


def userSearch(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		search = User.objects.filter(username__icontains=q)
		results = []
		for username_search in search:
			username_json = {}
			username_json = username_search.username
			results.append(username_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)

def createPost(request):
	if request.method == 'POST':
		# post = PostForm(request.user, request.POST, request.FILES)
		post_content = request.POST.get('post_content')
		post_activity = request.POST.get('post_activity')
		post_image = request.POST.get('post_image')
		response_data = {}

		post = Post(content=post_content, activity_id=post_activity, author=request.user)
		post.save()

		response_data['postpk'] = post.pk
		response_data['content'] = post.content
		response_data['activity'] = post.activity.id
		# response_data['image'] = post.image
		response_data['author'] = post.author.username
		response_data['date_posted'] = post.date_posted.strftime('%B %d, %Y %I:%M %p')
		# response_data['user_profile'] = request.user

		return HttpResponse(json.dumps(response_data), content_type="application/json")

	else:
		return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")





