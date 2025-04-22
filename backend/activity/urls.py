from django.urls import path
from .views import ActivityLogListAPIView, ActivityLogMarkReadAPIView

urlpatterns = [
    path('', ActivityLogListAPIView.as_view(), name='activity-log-list'),
    path('<int:pk>/mark_read/', ActivityLogMarkReadAPIView.as_view(), name='activity-log-mark-read'),
]
