from django.urls import path
from .views import (PostDetail, 
	PostUpdateView, PostDeleteView,
	IndexView)

from . import views

"""this file maps all our urls and displays them 
   path contains the arguments(url link, httpResponse(function in views.py), alias for url)
"""
app_name = "post"

urlpatterns = [
	path('', IndexView.as_view(), name='index-home'),
    path('home', views.home, name='blog-home'), 
    # path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('user/<str:username>/', views.UserPosts, name='user-posts'),
    # path('user/<str:username>/', PostListActivityView.as_view(), name='user-posts'), 
    path('post/<str:username>/<int:pk>/', views.PostDetail, name='post-detail'),
    path('create-post/', views.createPost, name='create-post'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), 
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('favorite/',views.favorite_post, name='favorite-post'), 
    path('<str:username>/favorites/', views.user_favorites, name='favorites_list'),
    path('like/',views.like_post, name='like-post'), 
    path('about', views.about, name='blog-about'),
    path('userssearch/', views.userSearch, name='search-users')
]
