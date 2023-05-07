from django.urls import path
from . import views

urlpatterns = [
	path('profile/<int:user_pk>/post/', views.profile_post_view, name='profile_post'),
	path('profile/<int:user_pk>/about/', views.profile_about_view, name='profile_about'),
]