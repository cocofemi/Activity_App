from django.urls import path
from .views import CommentDeleteView, CommentUpdateView, ReplyUpdateView 
from .import views 

app_name = "comment"

urlpatterns = [
	path('comment/<str:username>/<int:pk>/', views.PostComment, name='post-comment'),
	path('reply/comment/<int:pk>/', views.ReplyComment, name='reply-thread'),
	path('comment/<int:pk>/update', CommentUpdateView.as_view(), name='comment-update'),
	path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name='comment-delete'),
	path('reply/<int:pk>/update', ReplyUpdateView.as_view(), name='reply-update'),
	path('like/comment/<int:pk>/',views.like_comment, name='like-comment')
]