from django.urls import path
from . import views

urlpatterns = [
    path('group-create/', views.group_create_view, name='group_create'),
    path('<str:group>/', views.group_list_view, name='groups'),
    path('search/<str:group>/', views.group_list_view, name='search_groups'),
    path('group/<int:pk>/', views.group_detail_view, name='group_detail'),
    path('group/<int:group_pk>/join/', views.join_group_view, name='join_group'),
    path('group/<int:pk>/about/', views.group_about_view, name='group_about'),
    path('group/<int:pk>/members/', views.group_members_list_view, name='group_members'),
]