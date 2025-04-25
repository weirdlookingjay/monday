from rest_framework import serializers
from .models import AutomationCategory, AutomationTemplate, Automation
from boards.models import Board
from django.contrib.auth import get_user_model

class AutomationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomationCategory
        fields = ['id', 'name', 'slug', 'icon']

class AutomationTemplateSerializer(serializers.ModelSerializer):
    """
    Serializes AutomationTemplate objects, including:
    - id, category, name, description, supports_subitems, config_schema
    - default_conditions: Optional list of default condition objects for the template
    """
    category = AutomationCategorySerializer()
    class Meta:
        model = AutomationTemplate
        fields = ['id', 'category', 'name', 'description', 'supports_subitems', 'config_schema', 'default_conditions']

from accounts.serializers import UserSerializer

class AutomationSerializer(serializers.ModelSerializer):
    """
    The `config` field should be a dict with the following structure:
    {
        "trigger": string,              # e.g. "due_date_arrives"
        "conditions": [                 # optional, array of condition objects
            {"field": "status", "operator": "is", "value": "Working on it"},
            ...
        ],
        "action": string               # e.g. "notify_assignee"
    }
    """
    template = serializers.PrimaryKeyRelatedField(queryset=AutomationTemplate.objects.all())
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    user = UserSerializer()

    def validate_config(self, value):
        # Validate that config['conditions'] is a list if present
        if 'conditions' in value and not isinstance(value['conditions'], list):
            raise serializers.ValidationError("'conditions' must be a list of condition objects.")
        return value

    class Meta:
        model = Automation
        fields = ['id', 'name', 'description', 'template', 'board', 'user', 'config', 'active', 'created']
