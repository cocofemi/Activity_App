from django.urls import path

from activity.api.apiviews import UserActivityList, CreateActivity, ActivityList

urlpatterns = [
path('activitylist/<str:username>', UserActivityList.as_view(), name='user_activity_list'),
path('activity/<int:pk>', ActivityList.as_view(), name='activity'),
path('create/', CreateActivity.as_view(), name='create_activity'),
]