from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.get_task_stats, name='task-stats'),
    path('tasks/', views.create_task, name='create-task'),
    path('groups/', views.list_groups, name='list-groups'),
]
