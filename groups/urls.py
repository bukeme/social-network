from django.urls import path
from . import views

urlpatterns = [
    path('group-create/', views.group_create_view, name='group_create'),
    path('<str:group>/', views.group_list_view, name='groups'),
    path('<str:group>/', views.group_list_view, name='my_groups'),
]