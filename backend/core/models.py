from django.db import models
from accounts.models import User
from boards.models import Board, Item

# Create your models here.

class Notification(models.Model):
    """Notification model for user alerts."""
    TYPE_CHOICES = [
        ('mention', 'Mention'),
        ('assignment', 'Assignment'),
        ('due_soon', 'Due Soon'),
        ('update', 'Update'),
        ('share', 'Share'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    data = models.JSONField(default=dict)  # Additional context data
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

class Automation(models.Model):
    """Automation rule model."""
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='automations')
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    trigger_type = models.CharField(max_length=50)
    trigger_config = models.JSONField()
    action_type = models.CharField(max_length=50)
    action_config = models.JSONField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']

class Comment(models.Model):
    """Comment model for items."""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

class Tag(models.Model):
    """Tag model for items."""
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)  # Hex color code
    items = models.ManyToManyField(Item, related_name='tags')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
