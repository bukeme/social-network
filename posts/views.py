from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomePageView(LoginRequiredMixin, TemplateView):
	template_name = 'posts/home.html'

home_page_view = HomePageView.as_view()
