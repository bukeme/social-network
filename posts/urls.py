from django.urls import path 
from . import views 

urlpatterns = [
	path('', views.home_page_view, name='home'),
	path('<int:post_pk>/', views.home_page_view, name='home'),
	path('group-post/<int:group_pk>/create/', views.home_page_view, name='create_group_post'),
	path('post/<int:pk>/', views.post_detail_view, name='post_detail'),
	path('post/<int:pk>/edit/', views.post_edit_view, name='post_edit'),
	path('image/<int:image_pk>/delete/', views.delete_postimage_view, name='delete_postimage'),
	path('post-image/<int:post_pk>/add/', views.add_postimage_view, name='add_postimage'),
	path('post-image/<int:post_pk>/delete-all/', views.delete_all_postimage_view, name='delete_all_postimage'),
	path('post-video/<int:post_pk>/', views.post_video_view, name='post_video'),
	path('post/<int:post_pk>/delete/', views.post_delete_view, name='post_delete'),
	path('post/<int:post_pk>/like/', views.post_likes_view, name='post_like'),
	path('comment/<int:post_pk>/create/', views.comment_create_view, name='comment_create'),
	path('reply/<int:comment_pk>/create/', views.reply_create_view, name='reply_create'),
	path('comment/<int:comment_pk>/edit/', views.comment_edit_view, name='comment_edit'),
	path('reply/<int:reply_pk>/edit/', views.reply_edit_view, name='reply_edit'),
	path('comment/<int:comment_pk>/delete/', views.comment_delete_view, name='comment_delete'),
	path('reply/<int:reply_pk>/delete/', views.reply_delete_view, name='reply_delete'),
	path('comment/<int:comment_pk>/like/', views.comment_likes_view, name='comment_like'),
	path('reply/<int:reply_pk>/like/', views.reply_likes_view, name='reply_like'),
	# path('shared-post/<int:post_pk>/create/', views.shared_post_create_view, name='shared_post_create'),
]