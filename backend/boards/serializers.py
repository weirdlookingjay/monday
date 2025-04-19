from rest_framework import serializers
from .models import Board, Item, Group, Column, Activity
from django.contrib.auth import get_user_model

User = get_user_model()

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class TaskStatsSerializer(serializers.Serializer):
    """Serializer for task statistics."""
    total_tasks = serializers.IntegerField()
    tasks_in_progress = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    tasks_by_status = serializers.DictField()
    recent_tasks = serializers.ListField()

class ItemSerializer(serializers.ModelSerializer):
    """Serializer for board items."""
    class Meta:
        model = Item
        fields = ['id', 'created_by', 'created_at', 'updated_at', 'status', 'values']
