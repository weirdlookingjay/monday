from django.db import models
from django.conf import settings
from boards.models import Item  # Item is the task model

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    task = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, default='')

    def task_name(self):
        return self.task.values.get('name') if self.task and hasattr(self.task, 'values') else None

    def __str__(self):
        return f"{self.user} {self.action} {self.task_name()} at {self.timestamp}"

class ActivityLogRead(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    log = models.ForeignKey(ActivityLog, on_delete=models.CASCADE, related_name='reads')
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'log')
