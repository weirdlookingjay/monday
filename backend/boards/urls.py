from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.get_task_stats, name='task-stats'),
    path('tasks/', views.create_task, name='create-task'),
    path('groups/', views.list_groups, name='list-groups'),
    path('groups/create/', views.create_group, name='create-group'),
    path('list/', views.list_boards, name='list-boards'),
    path('create/', views.create_board, name='create-board'),
]
