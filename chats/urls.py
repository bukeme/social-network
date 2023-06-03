from django.urls import path
from . import views


urlpatterns = [
	path('', views.thread_view, name='threads'),
	path('<int:user_pk>/', views.thread_chat_view, name='thread_chat'),
	path('image-upload/<int:thread_pk>/', views.chat_image_upload_view, name='chat_image_upload'),
]