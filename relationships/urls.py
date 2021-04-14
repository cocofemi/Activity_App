from django.urls import path
from .views import UsersDisplayListView, FollowersDisplayListView, FollowingUserDisplayListView
from .import views 

app_name = "relationship"

urlpatterns = [
	path('follow/<str:username>', views.follow, name='follow_user'),
	path('unfollow/<str:username>', views.unfollow, name='unfollow_user'),
	path('users/list', UsersDisplayListView.as_view(), name='user-list'),
	path('find-and-add/', views.find_and_add, name='find_add_user'),
	path('<str:username>/followers', FollowersDisplayListView.as_view(), name='followers-list'),
	path('<str:username>/following', FollowingUserDisplayListView.as_view(), name='following-list')

]