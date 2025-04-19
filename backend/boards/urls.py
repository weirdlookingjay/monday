from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.list_users, name='list-users'),
    path('stats/', views.get_task_stats, name='task-stats'),
    path('tasks/', views.create_task, name='create-task'),
    path('tasks/<int:item_id>/', views.update_task, name='update-task'),
    path('groups/', views.list_groups, name='list-groups'),
    path('groups/create/', views.create_group, name='create-group'),
    path('groups/<int:group_id>/', views.update_group, name='update-group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete-group'),
    path('list/', views.list_boards, name='list-boards'),
    path('create/', views.create_board, name='create-board'),
]
