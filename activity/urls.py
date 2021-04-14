from django.urls import path
from .views import (ActivityListView, ActivityDeleteView, 
    ActivityDetailView, ActivityUpdateView, ActivityPostListView)
from . import views

"""this file maps all our urls and displays them 
   path contains the arguments(url link, httpResponse(function in views.py), alias for url)
"""

app_name = "activity"
urlpatterns = [
    path('user/<str:username>/activity/', ActivityListView.as_view(), name='activity-list'),
    path('activity/new/', views.CreateActivity, name='activity-create'),
    path('activity/<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),
    path('<str:username>/<int:pk>/<slug:slug>/', ActivityPostListView.as_view(), name='activitypost-detail'),
    path('bookmark_activity/<int:pk>', views.bookmark_activity, name='bookmark-activity'),
    path('activity/bookmarks/', views.bookmarks, name='bookmark-list'),
    path('activity/<int:pk>/<slug:slug>/update/', ActivityUpdateView.as_view(), name='activity-update'), 
    path('activity/<int:pk>/<slug:slug>/delete/', ActivityDeleteView.as_view(), name='activity-delete')
]
