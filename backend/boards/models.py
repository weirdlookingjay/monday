from django.db import models
from django.contrib.postgres.fields import JSONField
from accounts.models import User
from workspace.models import Workspace, WorkspaceFolder

class Board(models.Model):
    """Board model for managing tasks and items."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='boards')
    folder = models.ForeignKey(WorkspaceFolder, on_delete=models.SET_NULL, null=True, blank=True, related_name='boards')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_boards')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_boards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='todo')  # Added for kanban support
    
    VIEW_OPTIONS = [
        ('table', 'Table'),
        ('kanban', 'Kanban'),
        ('calendar', 'Calendar'),
        ('timeline', 'Timeline'),
        ('chart', 'Chart'),
    ]
    default_view = models.CharField(max_length=20, choices=VIEW_OPTIONS, default='table')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

class Column(models.Model):
    """Column definition for board items."""
    COLUMN_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('status', 'Status'),
        ('person', 'Person'),
        ('checkbox', 'Checkbox'),
        ('timeline', 'Timeline'),
        ('file', 'File'),
    ]
    
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=COLUMN_TYPES)
    settings = models.JSONField(default=dict)  # For storing column-specific settings
    position = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['position']
        unique_together = ['board', 'position']

class Group(models.Model):
    """Group of items within a board."""
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)  # Hex color code
    position = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['position']
        unique_together = ['board', 'position']

class Item(models.Model):
    """Individual item/task within a board group."""
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('stuck', 'Stuck'),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='items')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    position = models.PositiveIntegerField()
    values = models.JSONField(default=dict)  # Stores the values for each column
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    
    class Meta:
        ordering = ['position']
        unique_together = ['group', 'position']

class Activity(models.Model):
    """Activity log for board items."""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
