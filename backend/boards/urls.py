from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.get_task_stats, name='task-stats'),
]
