#file added c7, forms 
from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128,
						help_text="Please enter the category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)
	
	#Inline class to provide additional info on the form
	class Meta:
		#provide an association b/t ModelForm and model
		model = Category
		fields = ('name',)
		
class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128,
						help_text="Please enter the page name.")
	url = forms. URLField(max_length=200,
						help_text="Please enter the URL of the page.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	
	#"model metadata is anything that's not a field, 
	#(django docs / meta options)
	class Meta:
		model = Page
		# here decide which fields to include / exclude
		exclude = ('category', 'likes', 'slug',)
		#tried changing to just field, made form prettier
		# but then got errors on submission
		#fields = ('url',)
		
	#overriding clean input used in model forms
	# to accomodate for input imperfection
	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')
		
		if url and not url.startswith('http://'):
			url = 'http://' + url
			cleaned_data['url'] = url
			
			return cleaned_data

#c9 adding user auth and additional fields to user
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields =('website', 'picture')
			
			