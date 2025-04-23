from django.db import models
from django.conf import settings

class AutomationCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=100, blank=True)  # for UI icons

    def __str__(self):
        return self.name

class AutomationTemplate(models.Model):
    category = models.ForeignKey(AutomationCategory, on_delete=models.CASCADE, related_name='templates')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    supports_subitems = models.BooleanField(default=False)
    config_schema = models.JSONField(default=dict)  # structure for custom automation builder
    default_conditions = models.JSONField(null=True, blank=True, default=list, help_text="Optional default conditions for this template.")

    def __str__(self):
        return self.name

class Automation(models.Model):
    template = models.ForeignKey(AutomationTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    board = models.ForeignKey('boards.Board', on_delete=models.CASCADE, related_name='automation_automations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='automation_automations')
    config = models.JSONField(default=dict)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.template or 'Custom'} for {self.board}"
