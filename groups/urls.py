from django.urls import path
from . import views

urlpatterns = [
    path('group-search', views.group_search_view, name='group_search'),
    path('group-create/', views.group_create_view, name='group_create'),
    path('<str:group>/', views.group_list_view, name='groups'),
    path('search/<str:group>/', views.group_list_view, name='search_groups'),
    path('group/<int:pk>/', views.group_detail_view, name='group_detail'),
    path('group/<int:group_pk>/join/<int:user_pk>/', views.join_group_view, name='join_group'),
    path('group/<int:pk>/about/', views.group_about_view, name='group_about'),
    path('group/<int:pk>/members/', views.group_members_list_view, name='group_members'),
    path('group/<int:group_pk>/media/photos/', views.group_photos_view, name='group_photos'),
    path('group/<int:group_pk>/media/videos/', views.group_videos_view, name='group_videos'),
    path('group/<int:group_pk>/settings/', views.group_settings_view, name='group_settings'),
]