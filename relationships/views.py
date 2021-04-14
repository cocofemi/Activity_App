from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView
from .models import Relationship
from .util import get_people_user_follows, get_people_following_user
from .forms import SearchForm
from blog.models import Post
from activity.models import Activity
from notify.signals import notify

# Create your views here.
def _get_next(request):
    """
    1. If there is a variable named ``next`` in the *POST* parameters, the view will
    redirect to that variable's value.
    2. If there is a variable named ``next`` in the *GET* parameters, the view will
    redirect to that variable's value.
    3. If Django can determine the previous page from the HTTP headers, the view will
    redirect to that previous page.
    """
    return request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))

def follow(request, username):

	user = get_object_or_404(User, username=username)
	ul, created = Relationship.objects.get_or_create(from_user=request.user, 
		to_user=user)
	next = _get_next(request)
	if next and next != request.path:
		notify.send(request.user, recipient=user, actor=request.user, verb=' started following you', nf_type='followed_by_user')
		return redirect(next)
	context = {
		'other_user':user,
		'created': created
	}

	return render(request, 'relationship/followed.html', context)

def unfollow(request, username):

	user = get_object_or_404(User, username=username)
	try:
		ul = Relationship.objects.get(from_user=request.user, to_user=user)
		ul.delete()
		deleted = True
	except Relationship.doesNotExist:
		deleted = False
	next = _get_next(request)
	if next and next != request.path:
		# messages.success(request, ('You are no longer following %s ') % user.username)
		return redirect(next)

	context = {
		'other_user': user,
		'deleted': deleted
		}
	return(request, 'relationship/unfollowed.html', context)

def find_and_add(request):
    """
    A page for finding and adding new friends to follow.  Right now this
    consists solely of a search box, which given input, renders a list of
    users who match the search terms.
    """
    q = None 
    if request.method == 'GET':
	    search_form = SearchForm(request.GET or None)
	    if search_form.is_valid():
	        q = search_form.cleaned_data['q']
	        users = User.objects.filter(username__icontains=q) | User.objects.filter(
	            email__icontains=q)
	    else:
	        users = []
	    friends = get_people_user_follows(request.user)
	    users = [(u, u in friends) for u in users]

    context = {
    	'users': users,
    	'user_count': len(users),
    	'search_form': search_form,
    	'q': q
    }
    return render(request, 'relationship/find_add.html', context)

class UsersDisplayListView(ListView):
	model = User
	template_name = 'relationship/users_list_view.html'
	ordering = ['-date_joined']
	paginate_by = 25
	context_object_name = 'users'

class FollowersDisplayListView(ListView):
	model = Relationship
	template_name = 'relationship/followers_list.html'
	context_object_name = 'users'
	ordering = ['-date_added']

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		# users = get_people_user_follows(request.user)
		return get_people_following_user(user)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs) 
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		posts = Post.objects.filter(author=user).count()
		activities = Activity.objects.filter(author=user).count()
		following  = Relationship.objects.filter(from_user=user).count()
		followers  = Relationship.objects.filter(to_user=user).count()
		context['posts_count'] = posts
		context['activities_count'] = activities
		context['following_count'] = following
		context['followers_count'] = followers
		context['user_profile'] = user
		return context

class FollowingUserDisplayListView(ListView):
	model = Relationship
	template_name = 'relationship/following_list.html'
	context_object_name = 'users'

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return get_people_user_follows(user)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs) 
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		posts = Post.objects.filter(author=user).count()
		activities = Activity.objects.filter(author=user).count()
		following  = Relationship.objects.filter(from_user=user).count()
		followers  = Relationship.objects.filter(to_user=user).count()
		context['posts_count'] = posts
		context['activities_count'] = activities
		context['following_count'] = following
		context['followers_count'] = followers
		context['user_profile'] = user
		return context




