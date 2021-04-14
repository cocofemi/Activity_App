from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
	content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':3, 'placeholder':'Leave a comment...'}))
	image = forms.ImageField(label='', required=False)
	
	class Meta:
		model = Comment # User model to be affected 
		fields = ['content', 'image']

class ReplyForm(forms.ModelForm):
	content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':3, 'placeholder':'Leave a reply...'}))
	image = forms.ImageField(label='', required=False)
	
	class Meta:
		model = Comment # User model to be affected 
		fields = ['content', 'image']