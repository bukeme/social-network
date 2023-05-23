from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django import forms
from .models import UserProfile, ProfileImage, CoverImage


class UserSignUpForm(SignupForm):
	first_name = forms.CharField(max_length=200)
	last_name = forms.CharField(max_length=200)

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_class = 'mt-3'
		self.helper.layout = Layout(
			Div(
				Div('first_name', css_class='col'),
				Div('last_name', css_class='col'),
				css_class='form-row',
			),
			Div('email'),
			Div('username'),
			Div('password1'),
			Div('password2'),
			Submit('submit', 'Sign up', css_class='w-100 btn btn-primary'),
		)

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		exclude = ['id', 'user']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.required = False

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'username']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.required = False

class UserProfileSettingsForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['other_name', 'phone']

class UserProfileImageForm(forms.ModelForm):
	class Meta:
		model = ProfileImage
		fields = ['profile_image',]

class UserCoverImageForm(forms.ModelForm):
	class Meta:
		model = CoverImage
		fields = ['cover_image',]
