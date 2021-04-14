from django import forms
from .models import Post
from activity.models import Activity
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
	content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':3, 'placeholder':'Post in your activity'}))
	image = forms.ImageField(label='', required=False)
	
	class Meta:
		model = Post # User model to be affected 
		fields = ['content', 'activity', 'image']
		# widgets = {
		# 	'content': forms.Textarea(attrs={'rows':2, 'placeholder':'Drop a post in your activity'}, label=''),
		# }

	def __init__(self, user, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		self.fields['activity'] = forms.ModelChoiceField(queryset=Activity.objects.filter(author=user), label='', empty_label="Select Your Activity")

# class userSearchForm(forms.ModelForm):
# 	Search = forms.ModelChoiceField(
# 		queryset=User.objects.all(),
# 		widget=autocomplete.ModelSelect2(url='post:user-autocomplete')
# 		)

# 	class Meta:
# 		model = User
# 		fields = ()