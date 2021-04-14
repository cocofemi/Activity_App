from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Comment
from blog.models import Post
from .forms import CommentForm, ReplyForm
from notify.signals import notify

# Create your views here.

def PostComment(request, pk, username):
	post = get_object_or_404(Post, pk=pk)

	if request.method == 'POST':
		form = CommentForm(request.POST, request.FILES or None)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.author = request.user
			comment.post = post
			comment.save()
			return redirect('post:post-detail', username, pk)
	else:
		form = CommentForm()

	context = {
		'object': post,
		'form': form
	}

	return render(request, 'comments/post_comment.html', context)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Comment

	def test_func(self):
		comment = self.get_object()
		if self.request.user == comment.author:
			return True
		return False

	def get_success_url(self):
		post = self.object.post.id
		username = self.object.author
		return reverse('post:post-detail', kwargs={'username': username ,'pk': post})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Comment
	form_class = CommentForm
	template_name = 'comments/edit_comment.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.post_id = self.object.post.id
		form.instance.content = form.cleaned_data['content']
		return super().form_valid(form)

	def test_func(self):
		comment = self.get_object()
		if self.request.user == comment.author:
			return True
		return False
		
	def get_success_url(self):
		post = self.object.post.id
		username = self.object.author
		return reverse('post:post-detail', kwargs={'username':username, 'pk': post})

class ReplyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Comment
	form_class = CommentForm
	template_name = 'comments/reply_form.html'

	def test_func(self):
		comment = self.get_object()
		if self.request.user == comment.author:
			return True
		return False
		
	def get_success_url(self):
		post = self.object.post.id
		username = self.object.author
		return reverse('post:post-detail', kwargs={'username':username, 'pk': post})

def ReplyComment(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	form = ReplyForm(request.POST or None)
	if request.method == 'POST':
		reply_form = ReplyForm(request.POST, request.FILES or None)
		if reply_form.is_valid():
			Parent_obj = None
			try:
				Parent_id = int(request.POST.get('parent_id')) #get the id of the form 
			except:
				Parent_id = None
			if Parent_id: 
				Parent_obj = Comment.objects.get(id=Parent_id) #get the parent obj from the comment model passing in the id value
				if Parent_obj:
					reply_comment = reply_form.save(commit=False) #saves the comment as a reply to another comment on the main post not as a comment on the main post
					reply_comment.author = request.user #saves the author object as the logged in user
					reply_comment.parent = Parent_obj # saves the comment as a reply
					reply_comment.post_id = Parent_obj.post.id
					reply_comment.content = reply_form.cleaned_data.get('content')
					notify.send(request.user, recipient=comment.author, actor=request.user, 
							verb='replied your comment', target=reply_comment.parent, nf_type='reply_by_user')
					reply_comment.save()

					parts = reply_comment.content.split()
					for index, value in enumerate(parts):
						if value.startswith("@"):
							results = value[1:]
							try:
								user = User.objects.get(username=results)
								notify.send(request.user, recipient=user, actor=request.user, 
										verb='mentioned you in a reply', target=reply_comment, nf_type='mentioned_comment_by_user')
							except user.DoesNotExist: 
								return redirect('comment:reply-thread', Parent_obj.id)
					return redirect('comment:reply-thread', Parent_obj.id)
			# # comment = reply_form.save(commit=False) # if no parent id is gotten save the comment as a new comment to the main post 
			# # comment.author = request.user # save username of the logged in user
			# comment.post = Parent_obj.post.id # saves the pk of the current post 
			# # comment.save()
			# return redirect('comment:reply-thread', pk)
	else:
		reply_form = ReplyForm() #if no value is gotten return the form
	context = {
		'comment': comment,
		'form': form
	}

	return render(request, 'comments/reply_comment.html', context)

def like_comment(request, pk):
	comment = get_object_or_404(Comment, pk=pk)

	if comment.likes.filter(id=request.user.id).exists():
		 comment.likes.remove(request.user)
	else:
		comment.likes.add(request.user)
		notify.send(request.user, recipient=comment.author, actor=request.user, 
				verb='liked your comment', target=comment, nf_type='like_by_user')
	return HttpResponseRedirect(comment.get_absolute_url())


