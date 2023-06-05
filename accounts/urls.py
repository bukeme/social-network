from django.urls import path
from . import views

urlpatterns = [
	path('profile/<int:user_pk>/post/', views.profile_post_view, name='profile_post'),
	path('profile/<int:user_pk>/about/', views.profile_about_view, name='profile_about'),
	path('profile/<int:user_pk>/photos/', views.profile_photos_view, name='profile_photos'),
	path('userprofile/<int:user_pk>/update', views.update_user_profile_data_view, name='userprofile_update'),
	path('user/<int:user_pk>/update', views.update_user_data_view, name='user_update'),
	path('user/settings/', views.user_settings_view, name='user_settings'),
	path('user-profile/<int:user_pk>/update', views.update_user_profile_view, name='update_user_profile'),
	path('follow/<int:user_pk>/', views.follow_view, name='follow'),
	# path('followers-list/<int:user_pk>/', views.followers_list_view, name='followers_list'),
	path('follow-list/<int:user_pk>/<str:follow_type>/', views.follow_list_view, name='follow_list'),
	path('send-friend-request/<int:to_user_pk>/', views.send_friend_request_view, name='send_friend_request'),
	path('delete-friend-request/<int:to_user_pk>/<int:from_user_pk>/', views.delete_friend_request_view, name='delete_friend_request'),
	path('accept-friend-request/<int:from_user_pk>/', views.accept_friend_request_view, name='accept_friend_request'),
	path('friend-request-list/', views.friend_request_list_view, name='friend_request_list'),
	path('friend-list/<int:user_pk>/', views.friend_list_view, name='friend_list'),
	path('remove-friend/<int:user_pk>/', views.remove_friend_view, name='remove_friend'),
	path('user-search', views.user_search_view, name='user_search'),
]