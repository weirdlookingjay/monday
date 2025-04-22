from rest_framework import serializers
from .models import ActivityLog

from .models import ActivityLog, ActivityLogRead

class ActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    task_name = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = ActivityLog
        fields = ['id', 'user', 'action', 'task_name', 'timestamp', 'details', 'is_read']

    def get_task_name(self, obj):
        return obj.task_name()

    def get_is_read(self, obj):
        user = self.context['request'].user
        return ActivityLogRead.objects.filter(user=user, log=obj).exists()
