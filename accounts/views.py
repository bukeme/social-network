from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from allauth.account.views import SignupView
from accounts.forms import UserSignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class UserSignUpView(SignupView):
	form_class = UserSignUpForm

user_signup_view = UserSignUpView.as_view()

class ProfilePostView(LoginRequiredMixin, TemplateView):
	template_name = 'accounts/profile_post.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['user'] = get_object_or_404(User, pk=kwargs['user_pk'])
		context['page'] = 'profile_post'
		return context

profile_post_view = ProfilePostView.as_view()

class ProfileAboutView(LoginRequiredMixin, TemplateView):
	template_name = 'accounts/profile_about.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['user'] = get_object_or_404(User, pk=kwargs['user_pk'])
		context['page'] = 'profile_about'
		return context

profile_about_view = ProfileAboutView.as_view()
