from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django import forms


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