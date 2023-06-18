from django.urls import path
from . import views


urlpatterns = [
	path('', views.thread_view, name='threads'),
	path('<int:user_pk>/', views.thread_chat_view, name='thread_chat'),
	path('chat/<int:thread_pk>/create', views.chat_create_view, name='chat_create'),
]